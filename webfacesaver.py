import cv2
import numpy as np
import insightface
import os
import time
import logging
import albumentations as A
import collections
import argparse
from datetime import date
from yolox.tracker.byte_tracker import BYTETracker
from sklearn.metrics.pairwise import cosine_similarity
from database_utils import DatabaseUtils
from silentFaceSpoofing import SilentFaceAntiSpoofing
from face_saver import FaceSaver
from face_utils import FaceUtils
from concurrent.futures import ThreadPoolExecutor
from motion_clarity_utils import MotionClarityUtils

TF_ENABLE_ONEDNN_OPTS = 0
NO_ALBUMENTATIONS_UPDATE = 1
BASE_DIR = r"D:\Git Project\Face-Recognition"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


class TrackerArgs:
    def __init__(self):
        self.fps = 60
        self.track_thresh = 0.5
        self.track_buffer = 30
        self.match_thresh = 0.7
        self.min_box_area = 10
        self.aspect_ratio_thresh = 1.6


class AntiSpoofing:
    def __init__(self, face_detector):
        self.face_detector = face_detector
        self.anti_spoofing_model = SilentFaceAntiSpoofing(
            os.path.join(BASE_DIR, "weights/2.7_80x80_MiniFASNetV2.pth")
        )
        self.motion_clarity_utils = MotionClarityUtils()
        self.face_buffers = {}
        self.current_decisions = {}
        self.real_threshold = 0.7
        self.fake_threshold = 0.3
        self.hysteresis_margin = 0.1
        self.failure_counter = {}
        self.failure_threshold = 3

    def update_buffer(self, face_id, is_real):
        if face_id not in self.face_buffers:
            self.face_buffers[face_id] = collections.deque(maxlen=5)
        self.face_buffers[face_id].append(is_real)

    def get_final_decision(self, face_id):
        if face_id not in self.face_buffers or len(self.face_buffers[face_id]) < 5:
            return None
        weights = [1, 1, 1.5, 2, 2.5]
        buffer = self.face_buffers[face_id]
        weighted_sum = sum(w * result for w, result in zip(weights, buffer))
        total_weight = sum(weights[: len(buffer)])
        weighted_average = weighted_sum / total_weight

        if weighted_average > self.real_threshold:
            return "Real"
        elif weighted_average < self.fake_threshold:
            return "Fake"
        return None

    def extract_face(self, frame):
        try:
            detections, _ = self.face_detector.detect(frame, input_size=(128, 128))
            if detections is not None and len(detections) > 0:
                x1, y1, x2, y2, _ = map(int, detections[0])
                h, w = frame.shape[:2]
                x1, y1 = max(0, x1), max(0, y1)
                x2, y2 = min(w, x2), min(h, y2)
                if x2 > x1 and y2 > y1:
                    face_crop = frame[y1:y2, x1:x2]
                    return face_crop, (x1, y1, x2, y2)
            return None, None
        except Exception as e:
            logging.error(f"Error in extract_face: {e}")
            return None, None

    def analyze_frame(self, face_crop, face_id):
        try:
            is_real = self.anti_spoofing_model.predict(face_crop)
            self.update_buffer(face_id, is_real)

            if len(self.face_buffers[face_id]) == self.face_buffers[face_id].maxlen:
                weights = [1, 1, 1.5, 2, 2.5]
                weighted_sum = sum(w * result for w, result in zip(weights, self.face_buffers[face_id]))
                total_weight = sum(weights)
                weighted_average = weighted_sum / total_weight

                logging.info(f"Weighted Average for {face_id}: {weighted_average:.2f}")

                if self.current_decisions.get(face_id) == "Real":
                    if weighted_average < self.fake_threshold + self.hysteresis_margin:
                        self.current_decisions[face_id] = "Fake"
                elif self.current_decisions.get(face_id) == "Fake":
                    if weighted_average > self.real_threshold - self.hysteresis_margin:
                        self.current_decisions[face_id] = "Real"
                else:
                    if weighted_average > self.real_threshold:
                        self.current_decisions[face_id] = "Real"
                    elif weighted_average < self.fake_threshold:
                        self.current_decisions[face_id] = "Fake"

                logging.info(f"Final Decision for {face_id}: {self.current_decisions[face_id]}")
                return self.current_decisions[face_id]

            return None

        except Exception as e:
            logging.error(f"Error in analyze_frame for {face_id}: {e}")
            return None
        
    def liveness_check(self, face_crop, frame, bbox, face_id):
        try:
            if face_id not in self.failure_counter:
                self.failure_counter[face_id] = 0
            
            motion_valid = self.motion_clarity_utils.check_motion(frame, bbox=bbox)
            if not motion_valid:
                self.failure_counter[face_id] += 1
                logging.info(f"Face {face_id} failed motion check (relaxed).")
                return False, "No Motion"

            clarity_valid, clarity_score = self.motion_clarity_utils.check_clarity(face_crop)
            if not clarity_valid:
                self.failure_counter[face_id] += 1
                logging.info(f"Face {face_id} failed clarity check with score {clarity_score:.2f}.")
                return False, "Fake"
            
            if not self.motion_clarity_utils.analyze_texture(face_crop):
                self.failure_counter[face_id] += 1            
                return False, "Fake"
            
            if not self.motion_clarity_utils.analyze_frequency(face_crop):
                self.failure_counter[face_id] += 1
                return False, "Fake"

            is_real = self.anti_spoofing_model.predict(face_crop)
            if not is_real:
                logging.info(f"Face {face_id} classified as Fake by anti-spoofing model.")
                return False, "Fake"

            # Step 4: Return real status if all checks pass
            logging.info(f"Face {face_id} passed all liveness checks and classified as Real.")
            self.failure_counter[face_id] = 0
            return True, "Real"

        except Exception as e:
            logging.error(f"Error in liveness check for {face_id}: {e}")
            return False, "Error"

class FaceTracker:
    def __init__(self, detection_model_file, model, face_directory):
        self.face_labels = {}
        self.next_label = 1

        self.face_detector = insightface.model_zoo.SCRFD(
            model_file=detection_model_file
        )
        self.face_detector.prepare(ctx_id=0, input_size=(128, 128))
        self.recognition_model = insightface.model_zoo.get_model(
            r"C:\Users\User\.insightface\models\buffalo_l\w600k_r50.onnx"
        )
        self.recognition_model.prepare(ctx_id=0)
        self.anti_spoofing = AntiSpoofing(self.face_detector)
        self.db_utils = DatabaseUtils()
        self.face_data = {}
        self.face_db = {}
        args = TrackerArgs()
        self.tracker = BYTETracker(args, frame_rate=args.fps)
        self.last_logged_time = {}
        self.check_in_mode = True
        self.frame_skip = 2
        self.frame_count = 0
        self.augmentation_pipeline = A.Compose(
            [
                A.HorizontalFlip(p=0.5),
                A.Rotate(limit=10, p=0.5),
                A.RandomBrightnessContrast(p=0.5),
                A.Affine(
                    scale=(0.9, 1.1),
                    translate_percent=(0.0625, 0.0625),
                    rotate=(-10, 10),
                    p=0.5,
                ),
            ]
        )
        self.face_saver = FaceSaver(
            self.face_detector, self.augmentation_pipeline, self.recognition_model, self.db_utils
        )

    def identify_faces(self, embeddings):
        best_match = "Unknown"
        best_match_id = None
        highest_similarity = 0.0
        embeddings = np.squeeze(embeddings)
        
        if not self.face_db:
            return "Unknown", 0.0
        
        for (id, name), db_embedding in self.face_db.items():
            db_embedding = np.squeeze(db_embedding)
            similarity = cosine_similarity([db_embedding], [embeddings])[0][0]
            if similarity > highest_similarity:
                highest_similarity = similarity
                best_match = name
                best_match_id = id
        if highest_similarity > 0.6:
            return best_match, highest_similarity
        else:
            return "Unknown", highest_similarity
    
    def load_faces(self):
        face_db = {}

        for entry in self.face_data:
            if 'faces' not in entry:
                continue
            
            id = entry['id']
        
            for image_path in entry['faces']:
                person_name = os.path.basename(os.path.dirname(image_path))
                img = cv2.imread(os.path.join(BASE_DIR, image_path))
                if img is None:
                    print(f"Failed to load image: {os.path.join(BASE_DIR, image_path)}")
                    continue
                
                face, success = FaceUtils.get_face_embedding(
                    self.face_detector, self.recognition_model, img
                )
                if success:
                    key = (id, person_name)
                    if key not in face_db:
                        face_db[key] = []
                        
                    face_db[key] = face
                    print(f"Face embedding loaded for {person_name} from {os.path.join(BASE_DIR, image_path)}.")
                else:
                    print(f"Failed to process face embedding for: {os.path.join(BASE_DIR, image_path)}")

        return face_db

    def find_faces(self, frame):
        try:
            det, _ = self.face_detector.detect(img=frame, input_size=(128, 128))
            return det
        except Exception as e:
            logging.error(f"Error finding faces: {e}")
            return None

    def update_tracks(self, frame, detections):
        try:
            img_info = [frame.shape[0], frame.shape[1]]
            return self.tracker.update(
                output_results=detections,
                img_info=img_info,
                img_size=(frame.shape[0], frame.shape[1]),
            )
        except Exception as e:
            logging.error(f"Error updating tracks: {e}")
            return []

    def draw_annotations(self, frame, tracked_faces, names=[]):
        online_tlwhs = []
        online_ids = []
        args = TrackerArgs()
        for t in tracked_faces:
            vertical = t.tlwh[2] / t.tlwh[3] > args.aspect_ratio_thresh
            if t.tlwh[2] * t.tlwh[3] > args.min_box_area and not vertical:
                online_tlwhs.append(t.tlwh)
                online_ids.append(t.track_id)
        text_scale = 2
        text_thickness = 2
        line_thickness = 2
        for i, tlwh in enumerate(online_tlwhs):
            x1, y1, w, h = map(int, tlwh)
            intbox = (x1, y1, x1 + w, y1 + h)
            obj_id = online_ids[i]
            id_text = names[i] if i < len(names) else "Unknown"
            color = self.get_color(abs(obj_id))
            cv2.rectangle(
                frame, intbox[:2], intbox[2:], color=color, thickness=line_thickness
            )
            cv2.putText(
                frame,
                id_text,
                (x1, y1),
                cv2.FONT_HERSHEY_PLAIN,
                text_scale,
                (0, 0, 255),
                thickness=text_thickness,
            )
        return frame

    def get_color(self, idx):
        idx = idx * 3
        return ((37 * idx) % 255, (17 * idx) % 255, (29 * idx) % 255)

    def get_face_embedding(self, img):
        return FaceUtils.get_face_embedding(
            self.face_detector, self.recognition_model, img
        )
        
    def handle_frame(self, frame):
        frame = cv2.resize(frame, (640, 480))
        try:    
            detections, landmarks = self.face_detector.detect(frame, input_size=(128, 128))
            logging.info(f"Detections: {detections}")
            
            if detections is not None and len(detections) > 0:
                detections = np.array(detections)
                tracked_faces = self.update_tracks(frame, detections)
                self.update_face_labels(tracked_faces)

                with ThreadPoolExecutor() as executor:
                    futures = []
                    for tracked_face in tracked_faces:
                        x1, y1, w, h = map(int, tracked_face.tlwh[:4])
                        x2, y2 = x1 + w, y1 + h
                        if x2 <= x1 or y2 <= y1:
                            logging.warning(f"Invalid bounding box for tracker ID {tracked_face.track_id}, skipping.")
                            continue
                        
                        tracker_id = tracked_face.track_id
                        face_label = self.face_labels.get(tracker_id, "Unknown")
                        face_crop = frame[y1:y2, x1:x2]

                        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                        
                        futures.append(
                            executor.submit(
                                self.process_face, face_crop, frame, face_label, x1, y1, x2, y2
                            )
                        )
                    
                    for future in futures:
                        frame = future.result()
            else:
                logging.info("No faces detected.")
            
        except Exception as e:
            logging.error(f"Error handling frame: {e}")
        return frame

    
    def update_face_labels(self, tracked_faces):
        current_ids = {face.track_id for face in tracked_faces}
        self.face_labels = {
            track_id: label for track_id, label in self.face_labels.items() if track_id in current_ids
        }

        for face in tracked_faces:
            if face.track_id not in self.face_labels:
                self.face_labels[face.track_id] = f"face_{self.next_label}"
                self.next_label += 1

        sorted_labels = sorted(self.face_labels.items(), key=lambda x: x[0])
        self.face_labels = {k: f"face_{i+1}" for i, (k, _) in enumerate(sorted_labels)}

    def process_face(self, face_crop, frame, face_label, x1, y1, x2, y2):
        try:
            logging.info(f"Processing face at bbox: {(x1, y1, x2, y2)}")
            bbox = (x1, y1, x2, y2)
            is_real, decision = self.anti_spoofing.liveness_check(face_crop, frame, bbox, face_label)

            if decision == "No Motion":
                color = (0, 0, 255)
                label = f"{face_label}: Fake (No Motion)"
            elif decision == "Low Clarity":
                color = (0, 255, 255)
                label = f"{face_label}: Fake (Low Clarity)"
            elif decision == "Fake":
                color = (0, 0, 255)
                label = f"{face_label}: Fake"
            elif decision == "Real":
                face_embedding, success = self.get_face_embedding(face_crop)
                if success:
                    name, similarity = self.identify_faces(face_embedding)
                    color = (0, 255, 0)
                    label = f"{name} ({similarity:.2f})" if name != "Unknown" else "Real"
                else:
                    color = (255, 255, 0)
                    label = "Undecided"
            else:
                color = (255, 255, 0)
                label = decision

            # Annotate the frame with bounding box and label
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

            return frame
        except Exception as e:
            logging.error(f"Error processing face {face_label}: {e}")
            return frame


def main():
    parser = argparse.ArgumentParser(description="Face Recognition Script")
    parser.add_argument("name", type=str, help="Name of the subject")
    parser.add_argument("enrollment_number", type=str, help="Enrollment Number of the subject")
    parser.add_argument("faculty", type=str, help="Faculty of the subject")
    args = parser.parse_args()

    student_name = args.name
    enrollment_number = args.enrollment_number
    faculty = args.faculty
        
    detection_model_file = os.path.join(BASE_DIR, "weights/scrfd_2.5g_bnkps.onnx")
    model = "buffalo_l"
    face_directory = os.path.join(BASE_DIR, "faces")
    tracker = FaceTracker(detection_model_file, model, face_directory)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        logging.error("Error: Could not open webcam.")
        return

    cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
    cap.set(cv2.CAP_PROP_FOCUS, 70)

    while True:
        start_time = time.time()
        ret, frame = cap.read()
        if not ret:
            logging.error("Failed to grab frame.")
            break
        original_frame = frame.copy()
        annotated_frame = tracker.handle_frame(frame)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            tracker.face_saver.save_face_web(student_name, enrollment_number, faculty, original_frame, face_directory, cap)
            cap.release()
            cv2.destroyAllWindows()
        
        elapsed_time = time.time() - start_time
        fps = 1 / elapsed_time
        cv2.putText(
            frame,
            f"FPS: {fps:.2f}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )
        cv2.imshow("Face Tracking", annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

import cv2
import numpy as np
from yolox.tracker.byte_tracker import BYTETracker
import insightface
import os
import time
import logging
import threading
import asyncio
import sqlite3
from sklearn.metrics.pairwise import cosine_similarity
from insightface.utils import face_align
from aiohttp import web

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TrackerArgs:
    def __init__(self):
        self.fps = 60
        self.track_thresh = 0.5
        self.track_buffer = 30
        self.match_thresh = 0.7
        self.min_box_area = 10
        self.aspect_ratio_thresh = 1.6

class FaceTracker:
    def __init__(self, detection_model_file, model, face_directory, db_path):
        self.face_detector = insightface.model_zoo.SCRFD(
            model_file=detection_model_file
        )
        self.face_detector.prepare(ctx_id=0, input_size=(128, 128))

        self.recognition_model = insightface.model_zoo.get_model(
            r"C:\Users\User\.insightface\models\buffalo_l\w600k_r50.onnx"
        )
        self.recognition_model.prepare(ctx_id=0)

        self.face_db = self.load_face_database(face_directory)

        args = TrackerArgs()
        self.tracker = BYTETracker(args, frame_rate=args.fps)
        self.db_path = db_path
        self.init_db()
        self.last_logged_time = {}
        self.check_in_mode = True
        self.frame_skip = 2
        self.frame_count = 0

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS attendance
                          (name TEXT, status TEXT, timestamp TEXT)''')
        conn.commit()
        conn.close()

    def log_attendance(self, name):
        current_time = time.time()
        status = "Check-In" if self.check_in_mode else "Check-Out"
        if name not in self.last_logged_time or (current_time - self.last_logged_time[name]) > 5:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO attendance (name, status, timestamp) VALUES (?, ?, ?)",
                           (name, status, time.strftime('%Y-%m-%d %H:%M:%S')))
            conn.commit()
            conn.close()
            logging.info(f"Logged {status} for {name}")
            self.last_logged_time[name] = current_time

    def load_face_database(self, face_directory):
        face_db = {}
        for person_name in os.listdir(face_directory):
            person_dir = os.path.join(face_directory, person_name)
            if os.path.isdir(person_dir):
                for filename in os.listdir(person_dir):
                    if filename.endswith((".jpg", ".png")):
                        image_path = os.path.join(person_dir, filename)
                        img = cv2.imread(image_path)
                        if img is None:
                            continue

                        face, success = self.get_face_embedding(img)
                        if success:
                            face_db[person_name] = face
        return face_db

    def normalize(self, vector):
        norm = np.linalg.norm(vector)
        return vector / norm if norm > 0 else vector

    def recognize_faces(self, embeddings):
        best_match = "Unknown"
        highest_similarity = 0.0

        embeddings = np.squeeze(embeddings)
        for name, db_embedding in self.face_db.items():
            db_embedding = np.squeeze(db_embedding)
            similarity = cosine_similarity([db_embedding], [embeddings])[0][0]
            if similarity > highest_similarity:
                highest_similarity = similarity
                best_match = name

        if highest_similarity > 0.6:
            self.log_attendance(best_match)
            return best_match, highest_similarity
        else:
            return "Unknown", highest_similarity

    def detect_faces(self, frame):
        try:
            det, _ = self.face_detector.detect(img=frame, input_size=(128, 128))
            return det
        except Exception as e:
            logging.error(f"Error detecting faces: {e}")
            return None

    def track_faces(self, frame, detections):
        try:
            img_info = [frame.shape[0], frame.shape[1]]
            return self.tracker.update(
                output_results=detections,
                img_info=img_info,
                img_size=(frame.shape[0], frame.shape[1]),
            )
        except Exception as e:
            logging.error(f"Error tracking faces: {e}")
            return []

    def annotate_frame(self, frame, tracked_faces, names=[]):
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
        line_thickness = 3

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

    def align_face(self, image, landmarks):
        return face_align.norm_crop(image, landmark=landmarks)

    def get_face_embedding(self, img):
        try:
            detections, landmarks = self.face_detector.detect(
                img, input_size=(128, 128), max_num=1
            )

            if detections is not None and len(detections) > 0:
                x1, y1, x2, y2, confidence = map(int, detections[0])
                face_crop = img[y1:y2, x1:x2]

                if landmarks is not None and len(landmarks) > 0:
                    aligned_face = face_align.norm_crop(img, landmark=landmarks[0])
                    embedding = self.recognition_model.get_feat(aligned_face)
                    return self.normalize(embedding), True
        except Exception as e:
            logging.error(f"Error getting face embedding: {e}")
        return None, False

    def process_frame(self, frame):
        self.frame_count += 1
        if self.frame_count % self.frame_skip != 0:
            return frame

        try:
            detections, landmarks = self.face_detector.detect(frame, input_size=(128, 128))
            if detections is not None and len(detections) > 0:
                for i, det in enumerate(detections):
                    x1, y1, x2, y2, confidence = map(int, det)
                    face_crop = frame[y1:y2, x1:x2]

                    if landmarks is not None and i < len(landmarks):
                        face_embedding, success = self.get_face_embedding(face_crop)
                        if success:
                            name, similarity = self.recognize_faces(face_embedding)

                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                            cv2.putText(
                                frame,
                                f"{name} ({similarity:.2f})",
                                (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.6,
                                (0, 255, 0),
                                2,
                            )
        except Exception as e:
            logging.error(f"Error processing frame: {e}")
        return frame

    def save_face(self, name, img, face_directory):
        try:
            detections, landmarks = self.face_detector.detect(
                img, input_size=(128, 128), max_num=1
            )

            if detections is not None and len(detections) > 0:
                x1, y1, x2, y2, confidence = map(int, detections[0])
                face_crop = img[y1:y2, x1:x2]

                height, width, _ = img.shape
                x1 = max(0, x1)
                y1 = max(0, y1)
                x2 = min(width, x2)
                y2 = min(height, y2)

                face_embedding, success = self.get_face_embedding(face_crop)
                if success:
                    self.face_db[name] = face_embedding
                    person_dir = os.path.join(face_directory, name)
                    os.makedirs(person_dir, exist_ok=True)

                    image_count = len(os.listdir(person_dir))
                    face_path = os.path.join(person_dir, f"{name}_{image_count + 1}.jpg")

                    cv2.imwrite(face_path, face_crop)
                    logging.info(f"Face {name} registered successfully.")
                else:
                    logging.warning("Failed to register face. No face detected.")
            else:
                logging.warning("No faces detected in the input image.")
        except Exception as e:
            logging.error(f"Error saving face: {e}")

async def video_stream(tracker, cap):
    while True:
        ret, frame = cap.read()
        if not ret:
            logging.error("Failed to grab frame.")
            break

        annotated_frame = tracker.process_frame(frame)
        _, jpeg = cv2.imencode('.jpg', annotated_frame)
        frame_bytes = jpeg.tobytes()

        await asyncio.sleep(0.03)  # Simulate a delay for streaming

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

async def video_feed(request):
    tracker = request.app['tracker']
    cap = request.app['cap']
    return web.Response(body=video_stream(tracker, cap), content_type='multipart/x-mixed-replace; boundary=frame')

async def init_app():
    app = web.Application()
    app.router.add_get('/video_feed', video_feed)

    detection_model_file = "weights/scrfd_2.5g_bnkps.onnx"
    model = "buffalo_l"
    face_directory = "faces"
    db_path = "attendance.db"

    tracker = FaceTracker(detection_model_file, model, face_directory, db_path)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        logging.error("Error: Could not open webcam.")
        return

    app['tracker'] = tracker
    app['cap'] = cap

    return app

if __name__ == "__main__":
    web.run_app(init_app(), port=8081)

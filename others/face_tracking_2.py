import cv2
import numpy as np
from yolox.tracker.byte_tracker import BYTETracker
import insightface
import os
import time
from sklearn.metrics.pairwise import cosine_similarity
from insightface.utils import face_align

class TrackerArgs:
    def __init__(self):
        self.fps = 60
        self.track_thresh = 0.5
        self.track_buffer = 30
        self.match_thresh = 0.7
        self.min_box_area = 10
        self.aspect_ratio_thresh = 1.6

class FaceTracker:
    def __init__(self, detection_model_file, model, face_directory):
        self.face_detector = insightface.model_zoo.SCRFD(model_file=detection_model_file)
        self.face_detector.prepare(ctx_id=0, input_size=(128, 128))

        self.recognition_model = insightface.model_zoo.get_model(r"C:\Users\User\.insightface\models\buffalo_l\w600k_r50.onnx")
        self.recognition_model.prepare(ctx_id=0)

        self.face_directory = face_directory
        self.face_db = self.load_face_database(face_directory)

        args = TrackerArgs()
        self.tracker = BYTETracker(args, frame_rate=args.fps)

    def load_face_database(self, face_directory):
        face_db = {}
        for filename in os.listdir(face_directory):
            if filename.endswith((".jpg", ".png")):
                name = os.path.splitext(filename)[0]
                image_path = os.path.join(face_directory, filename)
                img = cv2.imread(image_path)
                if img is None:
                    print(f"Could not read image {filename}")
                    continue

                face, success = self.get_face_embedding(img)
                if success:
                    face_db[name] = face
                else:
                    print(f"No face detected in {filename}. Skipping.")
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

        return best_match if highest_similarity > 0.6 else "Unknown", highest_similarity

    def detect_faces(self, frame):
        det, _ = self.face_detector.detect(img=frame, input_size=(128, 128))
        return det

    def align_face(self, image, landmarks):
        return face_align.norm_crop(image, landmark=landmarks)

    def get_face_embedding(self, img):
        detections, landmarks = self.face_detector.detect(img, input_size=(128, 128), max_num=1)

        if detections is not None and len(detections) > 0:
            x1, y1, x2, y2, confidence = map(int, detections[0])
            face_crop = img[y1:y2, x1:x2]

            if landmarks is not None and len(landmarks) > 0:
                aligned_face = face_align.norm_crop(img, landmark=landmarks[0])
                embedding = self.recognition_model.get_feat(aligned_face)
                return self.normalize(embedding), True
            else:
                print("No landmarks detected for the face.")
        else:
            print("No faces detected in the input image.")
        return None, False

    def register_face(self, frame, name):
        """
        Register a new face into the database.
        :param frame: The current video frame from the camera.
        :param name: The name/ID to associate with the face.
        """
        detections, landmarks = self.face_detector.detect(frame, input_size=(128, 128), max_num=1)

        if detections is not None and len(detections) > 0:
            x1, y1, x2, y2, _ = map(int, detections[0])
            face_crop = frame[y1:y2, x1:x2]

            if landmarks is not None and len(landmarks) > 0:
                aligned_face = self.align_face(face_crop, landmarks[0])
                face_embedding = self.recognition_model.get_feat(aligned_face)

                # Normalize and save the embedding
                normalized_embedding = self.normalize(face_embedding)
                self.face_db[name] = normalized_embedding

                # Save the cropped face image to the face directory
                face_file = os.path.join(self.face_directory, f"{name}.jpg")
                cv2.imwrite(face_file, aligned_face)

                print(f"Successfully registered face: {name}")
            else:
                print("Could not detect landmarks for the face.")
        else:
            print("No faces detected in the frame.")

    def process_frame(self, frame):
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
                        cv2.putText(frame, f"{name} ({similarity:.2f})", (x1, y1 - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                else:
                    print("Landmarks missing for detected face.")
        else:
            print("No faces detected.")
        return frame

def main():
    detection_model_file = "weights/scrfd_2.5g_bnkps.onnx"
    model = "buffalo_l"
    face_directory = "faces"

    tracker = FaceTracker(detection_model_file, model, face_directory)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print("Press 'r' to register a new face, 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        annotated_frame = tracker.process_frame(frame)

        cv2.imshow("Face Registration and Tracking", annotated_frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('r'):
            print("Enter the name for the new face:")
            name = input()
            tracker.register_face(frame, name)
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

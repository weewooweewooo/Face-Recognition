import os
import cv2
import uuid
import logging
import albumentations as A
from database_utils import DatabaseUtils
from face_utils import FaceUtils


class FaceSaver:
    def __init__(self, face_detector, augmentation_pipeline, recognition_model, db_utils):
        self.face_detector = face_detector
        self.augmentation_pipeline = augmentation_pipeline
        self.recognition_model = recognition_model
        self.db_utils = db_utils
        self.face_db = {}

    def save_face(self, name, number, img, face_directory, cap, num_images=10):
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
                face_embedding, success = FaceUtils.get_face_embedding(
                    self.face_detector, self.recognition_model, face_crop
                )
                if success:
                    self.face_db[name] = face_embedding
                    person_dir = os.path.join(face_directory, name)
                    os.makedirs(person_dir, exist_ok=True)
                    file_paths = []
                    for i in range(num_images):
                        face_id = str(uuid.uuid4())
                        face_path = os.path.join(person_dir, f"{face_id}.jpg")
                        augmented = self.augmentation_pipeline(image=face_crop)
                        augmented_face = augmented['image']
                        cv2.imwrite(face_path, augmented_face)
                        logging.info(
                            f"Face {name} registered successfully as {face_path}."
                        )
                        file_paths.append(face_path)
                        ret, img = cap.read()
                        if not ret:
                            logging.error("Failed to grab frame for additional images.")
                            break
                        detections, landmarks = self.face_detector.detect(
                            img, input_size=(128, 128), max_num=1
                        )
                        if detections is not None and len(detections) > 0:
                            x1, y1, x2, y2, confidence = map(int, detections[0])
                            face_crop = img[y1:y2, x1:x2]
                        else:
                            logging.warning(
                                "No faces detected in the input image for additional images."
                            )
                            break
                    self.db_utils.save_face_to_db(name, number, "FIST", file_paths)
                else:
                    logging.warning("Failed to register face. No face detected.")
            else:
                logging.warning("No faces detected in the input image.")
        except Exception as e:
            logging.error(f"Error saving face: {e}")
            
    def save_face_web(self, name, enrollment_number, faculty, img, face_directory, cap, num_images=10):
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
                face_embedding, success = FaceUtils.get_face_embedding(
                    self.face_detector, self.recognition_model, face_crop
                )
                if success:
                    self.face_db[name] = face_embedding
                    person_dir = os.path.join(face_directory, name)
                    os.makedirs(person_dir, exist_ok=True)
                    file_paths = []
                    for i in range(num_images):
                        face_id = str(uuid.uuid4())
                        face_path = os.path.join(person_dir, f"{face_id}.jpg")
                        augmented = self.augmentation_pipeline(image=face_crop)
                        augmented_face = augmented['image']
                        cv2.imwrite(face_path, augmented_face)
                        logging.info(
                            f"Face {name} registered successfully as {face_path}."
                        )
                        file_paths.append(face_path)
                        ret, img = cap.read()
                        if not ret:
                            logging.error("Failed to grab frame for additional images.")
                            break
                        detections, landmarks = self.face_detector.detect(
                            img, input_size=(128, 128), max_num=1
                        )
                        if detections is not None and len(detections) > 0:
                            x1, y1, x2, y2, confidence = map(int, detections[0])
                            face_crop = img[y1:y2, x1:x2]
                        else:
                            logging.warning(
                                "No faces detected in the input image for additional images."
                            )
                            break
                    self.db_utils.save_face_to_db(name, enrollment_number, faculty, file_paths)
                else:
                    logging.warning("Failed to register face. No face detected.")
            else:
                logging.warning("No faces detected in the input image.")
        except Exception as e:
            logging.error(f"Error saving face: {e}")

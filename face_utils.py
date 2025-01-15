import cv2
import numpy as np
import logging
from insightface.utils import face_align

class FaceUtils:
    @staticmethod
    def align_face(image, landmarks):
        return face_align.norm_crop(image, landmark=landmarks)

    @staticmethod
    def normalize(vector):
        norm = np.linalg.norm(vector)
        return vector / norm if norm > 0 else vector

    @staticmethod
    def get_face_embedding(face_detector, recognition_model, img):
        try:
            detections, landmarks = face_detector.detect(
                img, input_size=(128, 128), max_num=1
            )
            if detections is not None and len(detections) > 0:
                x1, y1, x2, y2, confidence = map(int, detections[0])
                face_crop = img[y1:y2, x1:x2]
                if landmarks is not None and len(landmarks) > 0:
                    aligned_face = FaceUtils.align_face(img, landmarks[0])
                    embedding = recognition_model.get_feat(aligned_face)
                    return FaceUtils.normalize(embedding), True
        except Exception as e:
            logging.error(f"Error getting face embedding: {e}")
        return None, False

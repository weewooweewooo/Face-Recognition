import cv2
import numpy as np
from insightface.utils import face_align

class FaceDetection:
    def __init__(self, model, detector, recModel):
        self.detector = detector
        self.model = model
        self.recModel = recModel

    def detect_face(self, image):
        # Detect faces and landmarks using the SCRFD detector
        bboxes, kpss = self.detector.detect(image, input_size=(128, 128))
        return bboxes, kpss

    def align_face(self, image, landmarks):
        # Align face using the detected landmarks
        aligned_face = face_align.norm_crop(img=image, landmark=landmarks)
        return aligned_face

    def get_aligned_embedding(self, image):
        # Cropped Images
        # bboxes, kpss = self.detect_face(image)
        embedding = self.recModel.get_feat(image)
        embedding = np.squeeze(embedding)
        return embedding

    def get_embedding(self, image):
        # Raw Image
        faces = self.model.get(image)
        if faces is not None and len(faces) > 0:
            for face in faces:
                bbox = face['bbox']
                kps = face['kps']
                aligned_face = self.align_face(image, kps)
                aligned_face = cv2.resize(aligned_face, (112, 112))
                aligned_face = cv2.cvtColor(aligned_face, cv2.COLOR_BGR2RGB)

                embedding = self.recModel.get_feat(aligned_face)
                embedding = np.squeeze(embedding)
                return embedding
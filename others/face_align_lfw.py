import os
import cv2
import insightface
from insightface.utils import face_align

class FaceAligner:
    def __init__(self, detector, lfw_root, save_root):
        self.detector = detector
        self.lfw_root = lfw_root  # Root directory of the LFW dataset
        self.save_root = save_root  # Root directory to save aligned faces
        os.makedirs(self.save_root, exist_ok=True)

    def detect_faces(self, image):
        bboxes, kpss = self.detector.detect(image, input_size=(128, 128))
        return bboxes, kpss

    def align_face(self, image, landmarks):
        return face_align.norm_crop(img=image, landmark=landmarks)

    def align_and_save(self, image_path):
        # Read the image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Unable to read image {image_path}")
            return

        # Detect faces
        bboxes, kpss = self.detect_faces(image)
        if kpss is None or len(kpss) == 0:
            print(f"No faces detected in {image_path}")
            return

        # Align the first detected face
        aligned_face = self.align_face(image, kpss[0])

        # Preserve directory structure
        relative_path = os.path.relpath(image_path, start=self.lfw_root)
        output_path = os.path.join(self.save_root, relative_path)

        # Create directories as needed
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Save the aligned face
        cv2.imwrite(output_path, aligned_face)
        print(f"Aligned face saved to {output_path}")

    def process_images(self):
        # Walk through all subdirectories in the dataset root
        for root, dirs, files in os.walk(self.lfw_root):
            for file in files:
                if file.endswith(".jpg"):
                    image_path = os.path.join(root, file)
                    print(f"Processing: {image_path}")
                    self.align_and_save(image_path)


# Example usage
if __name__ == "__main__":
    lfw_root = "lfw-funneled/lfw_funneled"  # Root directory of the LFW dataset
    save_root = "lfw-funneled/aligned_faces"  # Root directory to save aligned faces
    detector = insightface.model_zoo.SCRFD(model_file="weights/scrfd_2.5g_bnkps.onnx")

    aligner = FaceAligner(detector=detector, lfw_root=lfw_root, save_root=save_root)
    aligner.process_images()

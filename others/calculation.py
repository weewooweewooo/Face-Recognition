import insightface
from recognition import Recognition
from detection import FaceDetection
import cv2
import os

def parse_pairs(pairs_file, dataset_path):
    pairs = []
    with open(pairs_file, "r") as f:
        lines = f.readlines()[1:]
        for line in lines:
            parts = line.strip().split()
            if len(parts) == 3:
                name, idx1, idx2 = parts
                img1 = os.path.join(dataset_path, name, f"{name}_{int(idx1):04d}.jpg")
                img2 = os.path.join(dataset_path, name, f"{name}_{int(idx2):04d}.jpg")
                pairs.append((img1, img2))
            elif len(parts) == 4:
                name1, idx1, name2, idx2 = parts
                img1 = os.path.join(dataset_path, name1, f"{name1}_{int(idx1):04d}.jpg")
                img2 = os.path.join(dataset_path, name2, f"{name2}_{int(idx2):04d}.jpg")
                pairs.append((img1, img2))
    return pairs

def initialize_model():
    model = insightface.app.FaceAnalysis("buffalo_l")
    model.prepare(ctx_id=0)

    arcface_model = insightface.model_zoo.get_model(r"C:\Users\User\.insightface\models\buffalo_l\w600k_r50.onnx")
    arcface_model.prepare(ctx_id=0)
    return model, arcface_model

if __name__ == "__main__":
    model, recModel = initialize_model()

    pairs_file = "pairs/pairs.txt"
    dataset_path = "lfw-funneled/lfw_funneled"
    dataset_path_aligned = "lfw-funneled/aligned_faces"

    pairs = parse_pairs(pairs_file, dataset_path)
    pairs_aligned = parse_pairs(pairs_file, dataset_path_aligned)

    detector = insightface.model_zoo.SCRFD(model_file="weights/scrfd_2.5g_bnkps.onnx")

    face_detector = FaceDetection(model, detector, recModel)
    recognition_calc = Recognition()

    for img1_path, img2_path in pairs[:1]:
        img1 = cv2.imread(img1_path)
        img2 = cv2.imread(img2_path)

        emb1 = face_detector.get_embedding(img1)
        emb2 = face_detector.get_embedding(img2)

        if emb1 is not None and emb2 is not None:
            cosine_sim = recognition_calc.calculate_similarity(emb1, emb2, method='cosine')
            euclidean_dist = recognition_calc.calculate_similarity(emb1, emb2, method='euclidean')
            manhattan_dist = recognition_calc.calculate_similarity(emb1, emb2, method='manhattan')
            dot_product = recognition_calc.calculate_similarity(emb1, emb2, method='dot')
            dot_product2 = recognition_calc.calculate_similarity(emb1, emb2, method='dot2')

            print(f"Results for {img1_path} and {img2_path}:")
            print(f"  Cosine Similarity: {cosine_sim}")
            print(f"  Euclidean Distance: {euclidean_dist}")
            print(f"  Manhattan Distance: {manhattan_dist}")
            print(f"  Dot Product: {dot_product}")
            print(f"  Dot Product Non-normalized embeddings: {dot_product2}")
        else:
            print(f"Face not detected in one or both images: {img1_path}, {img2_path}")

    for img1_path, img2_path in pairs_aligned[:1]:
        img1 = cv2.imread(img1_path)
        img2 = cv2.imread(img2_path)

        emb1 = face_detector.get_aligned_embedding(img1)
        emb2 = face_detector.get_aligned_embedding(img2)

        if emb1 is not None and emb2 is not None:
            cosine_sim = recognition_calc.calculate_similarity(emb1, emb2, method='cosine')
            euclidean_dist = recognition_calc.calculate_similarity(emb1, emb2, method='euclidean')
            manhattan_dist = recognition_calc.calculate_similarity(emb1, emb2, method='manhattan')
            dot_product = recognition_calc.calculate_similarity(emb1, emb2, method='dot')
            dot_product2 = recognition_calc.calculate_similarity(emb1, emb2, method='dot2')

            print(f"Results for {img1_path} and {img2_path}:")
            print(f"  Cosine Similarity: {cosine_sim}")
            print(f"  Euclidean Distance: {euclidean_dist}")
            print(f"  Manhattan Distance: {manhattan_dist}")
            print(f"  Dot Product: {dot_product}")
            print(f"  Dot Product Non-normalized embeddings: {dot_product2}")
        else:
            print(f"Face not detected in one or both images: {img1_path}, {img2_path}")


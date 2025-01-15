import numpy as np

class Recognition:
    def calculate_similarity(self, emb1, emb2, method='cosine'):
        if method == 'cosine':
            return self.cosine_similarity(emb1, emb2)
        elif method == 'euclidean':
            return self.euclidean_distance(emb1, emb2)
        elif method == 'manhattan':
            return self.manhattan_distance(emb1, emb2)
        elif method == 'dot':
            return self.dot_product_similarity(emb1, emb2)
        elif method == 'dot2':
            return self.dot_product_similarity2(emb1, emb2)
        else:
            raise ValueError(f"Unknown similarity method: {method}")

    def cosine_similarity(self, emb1, emb2):
        similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
        return max(0, similarity * 100)

    def euclidean_distance(self, emb1, emb2, max_distance=50):
        distance = np.linalg.norm(emb1 - emb2)
        return max(0, (1 - distance / max_distance) * 100)

    def manhattan_distance(self, emb1, emb2, max_distance=1000):
        distance = np.sum(np.abs(emb1 - emb2))
        return max(0, (1 - distance / max_distance) * 100)

    def dot_product_similarity(self, emb1, emb2):
        similarity = np.dot(emb1, emb2)
        return max(0, min(similarity, 1)) * 100

    def dot_product_similarity2(self, emb1, emb2, min_value=0, max_value=500):
        similarity = np.dot(emb1, emb2)
        normalized_score = (similarity - min_value) / (max_value - min_value)
        return max(0, min(normalized_score, 1)) * 100

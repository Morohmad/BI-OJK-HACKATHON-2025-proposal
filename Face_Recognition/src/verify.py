import pickle
import numpy as np
from deepface import DeepFace

from .config import (
    EMBEDDING_FILE,
    MODEL_NAME,
    DETECTOR_BACKEND,
    SIMILARITY_THRESHOLD,
)


class FaceVerifier:

    def __init__(self):

        print("Loading face embeddings...")

        with open(EMBEDDING_FILE, "rb") as file:
            self.database = pickle.load(file)

        print(f"{len(self.database)} identities loaded.\n")

    @staticmethod
    def cosine_distance(embedding1, embedding2):

        embedding1 = np.array(embedding1)
        embedding2 = np.array(embedding2)

        similarity = np.dot(embedding1, embedding2) / (
            np.linalg.norm(embedding1) * np.linalg.norm(embedding2)
        )

        return 1 - similarity

    def verify(self, frame):

        # Generate embedding dari webcam
        result = DeepFace.represent(
            img_path=frame,
            model_name=MODEL_NAME,
            detector_backend=DETECTOR_BACKEND,
            enforce_detection=False,
        )

        query_embedding = np.array(result[0]["embedding"])

        best_name = None
        best_distance = float("inf")

        # Bandingkan dengan setiap identitas
        for name, data in self.database.items():

            distance = self.cosine_distance(
                query_embedding,
                data["embedding"]
            )

            if distance < best_distance:
                best_distance = distance
                best_name = name

        # Jika melewati threshold → tidak terdaftar
        if best_distance > SIMILARITY_THRESHOLD:
            return False, "-", best_distance

        return True, best_name, best_distance
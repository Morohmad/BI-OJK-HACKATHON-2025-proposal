import os
from deepface import DeepFace

from config import (
    DATABASE_PATH,
    MODEL_NAME,
    DETECTOR_BACKEND,
)


class FaceRecognizer:

    def __init__(self):
        self.model_name = MODEL_NAME
        self.detector_backend = DETECTOR_BACKEND
        self.database_path = DATABASE_PATH

    def verify(self, frame):

        # ==========================
        # Cek folder database
        # ==========================
        if not os.path.exists(self.database_path):
            raise FileNotFoundError(
                f"Database tidak ditemukan:\n{self.database_path}"
            )

        folders = [
            f for f in os.listdir(self.database_path)
            if os.path.isdir(os.path.join(self.database_path, f))
        ]

        if len(folders) == 0:
            raise ValueError("Folder database masih kosong.")

        print("=" * 50)
        print("FACE RECOGNITION")
        print("=" * 50)
        print(f"Database : {self.database_path}")
        print(f"Jumlah identitas : {len(folders)}")
        print("Memulai pencocokan wajah...")
        print("=" * 50)

        try:

            result = DeepFace.find(
                img_path=frame,
                db_path=self.database_path,
                model_name=self.model_name,
                detector_backend=self.detector_backend,
                enforce_detection=False,
                silent=False,
            )

        except Exception as e:
            raise RuntimeError(
                f"DeepFace.find() gagal.\n{str(e)}"
            )

        print("Pencocokan selesai.")

        # ==========================
        # Tidak ditemukan
        # ==========================
        if len(result) == 0:
            return False, "-", None

        if len(result[0]) == 0:
            return False, "-", None

        # ==========================
        # Ambil hasil terbaik
        # ==========================
        best_match = result[0].iloc[0]

        identity = best_match["identity"]
        distance = float(best_match["distance"])

        filename = os.path.basename(identity)
        name = os.path.splitext(filename)[0]

        print(f"Identity : {identity}")
        print(f"Distance : {distance:.4f}")
        print("=" * 50)

        return True, name, distance
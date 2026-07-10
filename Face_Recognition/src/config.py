import os

# Root project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database wajah
DATABASE_PATH = os.path.join(BASE_DIR, "database")

# Folder model
MODEL_DIR = os.path.join(BASE_DIR, "models")

# Folder log
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "log_verifikasi.txt")

# AI Model
MODEL_NAME = "Facenet"

# Kamera
CAMERA_INDEX = 0

# Face detector
DETECTOR_BACKEND = "opencv"

# Threshold
THRESHOLD = 0.40

# Folder embeddings
EMBEDDING_DIR = os.path.join(BASE_DIR, "embeddings")
EMBEDDING_FILE = os.path.join(EMBEDDING_DIR, "face_embeddings.pkl")

# Similarity threshold
SIMILARITY_THRESHOLD = 0.30
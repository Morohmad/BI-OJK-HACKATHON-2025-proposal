import os
import time
import pickle
import numpy as np
from deepface import DeepFace

from .config import (
    DATABASE_PATH,
    EMBEDDING_DIR,
    EMBEDDING_FILE,
    MODEL_NAME,
    DETECTOR_BACKEND,
)


def get_mean_embedding(embeddings):
    """
    Menghitung rata-rata embedding dari beberapa foto.
    """
    return np.mean(np.array(embeddings), axis=0)


def enroll():

    start_time = time.time()

    os.makedirs(EMBEDDING_DIR, exist_ok=True)

    database = {}

    total_person = 0
    total_image = 0

    print("=" * 60)
    print("FACE ENROLLMENT")
    print("=" * 60)

    folders = sorted(os.listdir(DATABASE_PATH))

    for person in folders:

        person_path = os.path.join(DATABASE_PATH, person)

        if not os.path.isdir(person_path):
            continue

        print(f"\nProcessing : {person}")

        embeddings = []

        for image_name in os.listdir(person_path):

            if not image_name.lower().endswith(
                (".jpg", ".jpeg", ".png")
            ):
                continue

            image_path = os.path.join(person_path, image_name)

            try:

                result = DeepFace.represent(
                    img_path=image_path,
                    model_name=MODEL_NAME,
                    detector_backend=DETECTOR_BACKEND,
                    enforce_detection=False,
                )

                embedding = result[0]["embedding"]

                embeddings.append(embedding)

                total_image += 1

                print(f"   ✓ {image_name}")

            except Exception as e:

                print(f"   ✗ {image_name}")
                print(e)

        if len(embeddings) == 0:

            print("   Tidak ada wajah yang valid.")
            continue

        database[person] = {

            "embedding": get_mean_embedding(embeddings),
            "num_images": len(embeddings)

        }

        total_person += 1

    with open(EMBEDDING_FILE, "wb") as file:

        pickle.dump(database, file)

    elapsed = time.time() - start_time

    print("\n" + "=" * 60)
    print("ENROLLMENT FINISHED")
    print("=" * 60)
    print(f"Identity        : {total_person}")
    print(f"Images          : {total_image}")
    print(f"Output          : {EMBEDDING_FILE}")
    print(f"Processing Time : {elapsed:.2f} sec")
    print("=" * 60)


if __name__ == "__main__":
    enroll()
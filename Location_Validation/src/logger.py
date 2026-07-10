import os
from datetime import datetime

from config import LOG_DIR, LOG_FILE


class LocationLogger:

    def __init__(self):
        os.makedirs(LOG_DIR, exist_ok=True)

    def save(self, location, status, distance):

        with open(LOG_FILE, "a", encoding="utf-8") as f:

            f.write(
                f"{datetime.now()} | "
                f"{location} | "
                f"{status} | "
                f"{distance:.2f} m\n"
            )
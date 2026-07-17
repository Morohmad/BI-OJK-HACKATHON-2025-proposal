from .utils import get_timestamp, ensure_directory
from .config import LOG_DIR, LOG_FILE


class VerificationLogger:

    def __init__(self):
        ensure_directory(LOG_DIR)

    def save(self, name, status, distance=None):

        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(
                f"{get_timestamp()} | "
                f"Name: {name} | "
                f"Status: {status} | "
                f"Distance: {distance}\n"
            )
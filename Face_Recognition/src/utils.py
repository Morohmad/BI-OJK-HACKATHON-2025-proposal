import cv2
import os
from datetime import datetime


def draw_text(
    frame,
    text,
    position=(20, 40),
    color=(0, 255, 0),
    font_scale=1,
    thickness=2
):
    """
    Menampilkan teks pada frame.
    """
    cv2.putText(
        frame,
        text,
        position,
        cv2.FONT_HERSHEY_SIMPLEX,
        font_scale,
        color,
        thickness,
    )


def draw_rectangle(
    frame,
    x,
    y,
    w,
    h,
    color=(0, 255, 0),
    thickness=2,
):
    """
    Menggambar bounding box pada wajah.
    """
    cv2.rectangle(
        frame,
        (x, y),
        (x + w, y + h),
        color,
        thickness,
    )


def distance_to_confidence(distance):
    """
    Mengubah nilai distance menjadi confidence (%).
    """
    if distance is None:
        return 0.0

    confidence = max(0.0, min(100.0, (1 - distance) * 100))
    return round(confidence, 2)


def get_timestamp():
    """
    Menghasilkan timestamp saat ini.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def ensure_directory(path):
    """
    Membuat folder jika belum ada.
    """
    os.makedirs(path, exist_ok=True)
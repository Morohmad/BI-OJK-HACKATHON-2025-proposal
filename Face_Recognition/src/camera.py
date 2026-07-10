import cv2
from config import CAMERA_INDEX


class Camera:

    def __init__(self):
        self.cam = cv2.VideoCapture(CAMERA_INDEX)

        if not self.cam.isOpened():
            raise Exception("Camera cannot be opened.")

    def read(self):
        return self.cam.read()

    def release(self):
        self.cam.release()

    @staticmethod
    def show(window_name, frame):
        cv2.imshow(window_name, frame)

    @staticmethod
    def wait(delay=1):
        return cv2.waitKey(delay)

    @staticmethod
    def close():
        cv2.destroyAllWindows()
import cv2

from camera import Camera
from verify import FaceVerifier
from logger import VerificationLogger


camera = Camera()
recognizer = FaceVerifier()
logger = VerificationLogger()

WINDOW_NAME = "Face Recognition"

print("====================================")
print(" Face Recognition System")
print("====================================")
print("Press C to Verify")
print("Press ESC to Exit")

while True:

    ret, frame = camera.read()

    if not ret:
        break

    Camera.show(WINDOW_NAME, frame)

    key = Camera.wait(1)

    if key == 27:
        break

    elif key == ord("c"):

        print("Verifying...")

        verified, name, distance = recognizer.verify(frame)

        if verified:

            status = "VERIFIED"

            text = f"{name}"

            color = (0,255,0)

        else:

            status = "FAILED"

            text = "Unknown"

            color = (0,0,255)

        logger.save(name, status, distance)

        cv2.putText(
            frame,
            text,
            (20,40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            color,
            2
        )

        Camera.show(WINDOW_NAME, frame)

        Camera.wait(3000)

        break


camera.release()
Camera.close()
import cv2
import sys

from camera.camera_manager import CameraManager
from recognition.face_detector import FaceDetector
from recognition.face_database import FaceDatabase

from config import REGISTERED_FACES_DIR

from utils.helpers import (
    normalize_face,
    validate_user_id,
    validate_user_name
)


def register_faces():

    print("\n")
    print("=" * 45)
    print(" VJAYA ROBOTICS - FACE REGISTRATION")
    print("=" * 45)

    user_id = input("Enter User ID (numbers only): ").strip()

    if not validate_user_id(user_id):
        print("[ERROR] Invalid user ID.")
        return

    name = input("Enter person's name: ").strip()

    if not validate_user_name(name):
        print("[ERROR] Invalid name.")
        return

    database = FaceDatabase(REGISTERED_FACES_DIR)

    if user_id in database.get_users():
        print("[ERROR] User ID already registered.")
        return

    camera = CameraManager()
    detector = FaceDetector()

    captured_faces = []

    try:

        if not camera.start():
            print("[ERROR] Camera could not start.")
            return

        print("\nPosition your face in front of the camera.")
        print("Press SPACE to capture a face image.")
        print("Capture at least 20 images.")
        print("Press Q to cancel.\n")

        while len(captured_faces) < 30:

            frame = camera.capture_frame()

            if frame is None:
                continue

            gray, faces = detector.detect_faces(frame)

            for coordinates in faces:

                x, y, width, height = coordinates

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + width, y + height),
                    (0, 255, 0),
                    2
                )

            cv2.putText(
                frame,
                f"Captured: {len(captured_faces)}/30",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

            cv2.imshow(
                "Face Registration",
                frame
            )

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                print("[REGISTRATION] Cancelled.")
                return

            if key == 32:

                if len(faces) != 1:
                    print(
                        "[WARNING] Keep exactly one face "
                        "visible in the camera."
                    )
                    continue

                face_image = normalize_face(
                    gray,
                    faces[0]
                )

                if face_image is not None:

                    captured_faces.append(
                        face_image.copy()
                    )

                    print(
                        f"[CAPTURED] "
                        f"{len(captured_faces)}/30"
                    )

        if len(captured_faces) >= 20:

            saved = database.register_user(
                user_id,
                name,
                captured_faces
            )

            print("\n[REGISTRATION SUCCESSFUL]")
            print(f"User ID: {user_id}")
            print(f"Name: {name}")
            print(f"Images saved: {saved}")

    finally:

        camera.stop()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    register_faces()
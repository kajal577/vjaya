import cv2
import time
import sys

from config import (
    REGISTERED_FACES_DIR,
    REQUIRED_MATCH_FRAMES,
    ENABLE_ACCESS_LOGGING
)

from camera.camera_manager import CameraManager

from recognition.face_detector import FaceDetector
from recognition.face_recognizer import FaceRecognizer
from recognition.face_database import FaceDatabase

from hardware.door_lock import DoorLock
from hardware.manual_override import ManualOverride
from hardware.buzzer import AccessBuzzer
from hardware.display import StatusDisplay

from security.access_control import AccessControl
from security.access_logger import AccessLogger

from utils.helpers import (
    normalize_face,
    draw_face_box
)


def main():

    print("\n")
    print("=" * 50)
    print(" VJAYA ROBOTICS")
    print(" AI FACE RECOGNITION DOOR ACCESS SYSTEM")
    print("=" * 50)

    camera = None
    door_lock = None
    manual_override = None
    buzzer = None
    display = None
    logger = None

    try:

        # ==========================================
        # INITIALIZE HARDWARE
        # ==========================================

        door_lock = DoorLock()
        door_lock.lock()

        buzzer = AccessBuzzer()
        display = StatusDisplay()

        logger = AccessLogger()

        access_control = AccessControl(
            door_lock,
            buzzer,
            display,
            logger
        )

        manual_override = ManualOverride(
            door_lock,
            callback=access_control.manual_unlock
        )

        # ==========================================
        # INITIALIZE FACE DATABASE
        # ==========================================

        face_database = FaceDatabase(
            REGISTERED_FACES_DIR
        )

        training_images, training_labels = (
            face_database.load_training_data()
        )

        if not training_images:

            print(
                "[ERROR] No registered faces found."
            )

            print(
                "Run register_faces.py first."
            )

            return

        # ==========================================
        # TRAIN RECOGNITION MODEL
        # ==========================================

        recognizer = FaceRecognizer()

        recognizer.train(
            training_images,
            training_labels
        )

        print("[AI] Face recognition model trained.")

        # ==========================================
        # INITIALIZE DETECTOR
        # ==========================================

        detector = FaceDetector()

        # ==========================================
        # START CAMERA
        # ==========================================

        camera = CameraManager()

        if not camera.start():

            print("[ERROR] Camera initialization failed.")

            return

        display.show_locked()

        print("\n[SYSTEM] Door access system running.")
        print("[SYSTEM] Press Q to quit.")
        print("[SYSTEM] Manual override button is active.")

        # ==========================================
        # FACE TRACKING VARIABLES
        # ==========================================

        matched_user = None
        match_count = 0

        last_denial_time = 0
        denial_cooldown = 5

        last_granted_user = None

        # ==========================================
        # MAIN PROCESSING LOOP
        # ==========================================

        while True:

            frame = camera.capture_frame()

            if frame is None:
                time.sleep(0.1)
                access_control.update()
                continue

            gray, faces = detector.detect_faces(frame)

            access_control.update()

            if len(faces) == 0:

                matched_user = None
                match_count = 0
                last_granted_user = None

            for coordinates in faces:

                face_image = normalize_face(
                    gray,
                    coordinates
                )

                if face_image is None:
                    continue

                user_id, confidence = recognizer.recognize(
                    face_image
                )

                if user_id is not None:

                    user_name = face_database.get_user_name(
                        user_id
                    )

                    if user_name:

                        if matched_user == user_id:
                            match_count += 1
                        else:
                            matched_user = user_id
                            match_count = 1

                        draw_face_box(
                            frame,
                            coordinates,
                            f"{user_name}: MATCH"
                        )

                        if (
                            match_count >= REQUIRED_MATCH_FRAMES
                            and last_granted_user != user_id
                        ):

                            granted = access_control.grant_access(
                                user_name,
                                user_id
                            )

                            if granted:
                                last_granted_user = user_id

                else:

                    matched_user = None
                    match_count = 0
                    last_granted_user = None

                    draw_face_box(
                        frame,
                        coordinates,
                        "UNKNOWN - ACCESS DENIED",
                        (0, 0, 255)
                    )

                    current_time = time.monotonic()

                    if (
                        current_time - last_denial_time
                        >= denial_cooldown
                    ):

                        access_control.deny_access()

                        last_denial_time = current_time

            cv2.imshow(
                "VJaYa AI Door Access System",
                frame
            )

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

    except KeyboardInterrupt:

        print("\n[SYSTEM] Shutdown requested.")

    except Exception as error:

        print(f"\n[SYSTEM ERROR] {error}")

    finally:

        print("[SYSTEM] Cleaning up hardware...")

        if camera:
            camera.stop()

        if manual_override:
            manual_override.cleanup()

        if door_lock:
            door_lock.cleanup()

        if buzzer:
            buzzer.cleanup()

        if display:
            display.cleanup()

        if logger:
            logger.close()

        cv2.destroyAllWindows()

        print("[SYSTEM] Shutdown complete.")


if __name__ == "__main__":
    main()
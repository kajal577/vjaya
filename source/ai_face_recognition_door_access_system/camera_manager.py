import cv2
from picamera2 import Picamera2

from config import (
    CAMERA_WIDTH,
    CAMERA_HEIGHT,
    CAMERA_FRAME_RATE
)


class CameraManager:

    def __init__(self):
        self.camera = None
        self.running = False

    def start(self):
        try:
            self.camera = Picamera2()

            camera_config = self.camera.create_video_configuration(
                main={
                    "size": (CAMERA_WIDTH, CAMERA_HEIGHT),
                    "format": "RGB888"
                }
            )

            self.camera.configure(camera_config)
            self.camera.start()

            self.running = True

            print("[CAMERA] Camera started successfully.")

            return True

        except Exception as error:
            print(f"[CAMERA ERROR] {error}")
            self.camera = None
            return False

    def capture_frame(self):
        if not self.running or self.camera is None:
            return None

        try:
            frame = self.camera.capture_array()

            return cv2.cvtColor(
                frame,
                cv2.COLOR_RGB2BGR
            )

        except Exception as error:
            print(f"[CAMERA ERROR] Frame capture failed: {error}")
            return None

    def stop(self):
        if self.camera is not None:
            self.camera.stop()
            self.camera.close()

        self.camera = None
        self.running = False

        print("[CAMERA] Camera stopped.")
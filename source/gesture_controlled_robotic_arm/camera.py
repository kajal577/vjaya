
"""
GESTURE CONTROLLED ROBOTIC ARM
File: camera.py

Camera initialization and video capture.
"""

import cv2

from config import (
    CAMERA_INDEX,
    CAMERA_WIDTH,
    CAMERA_HEIGHT,
    CAMERA_FPS,
    MIRROR_CAMERA,
)


class Camera:
    def __init__(self):
        self.camera = None

    def start(self):
        """Initialize and start the camera."""

        self.camera = cv2.VideoCapture(CAMERA_INDEX)

        if not self.camera.isOpened():
            raise RuntimeError(
                "Camera could not be opened. "
                "Check the webcam connection and CAMERA_INDEX."
            )

        self.camera.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            CAMERA_WIDTH
        )

        self.camera.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            CAMERA_HEIGHT
        )

        self.camera.set(
            cv2.CAP_PROP_FPS,
            CAMERA_FPS
        )

        print("Camera started successfully.")

    def read(self):
        """Capture and return one camera frame."""

        if self.camera is None:
            return None

        success, frame = self.camera.read()

        if not success:
            return None

        if MIRROR_CAMERA:
            frame = cv2.flip(frame, 1)

        return frame

    def stop(self):
        """Release the camera."""

        if self.camera is not None:
            self.camera.release()
            self.camera = None

        cv2.destroyAllWindows()

        print("Camera stopped.")

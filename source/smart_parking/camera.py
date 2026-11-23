
"""
============================================================
VJaYa Robotics
PROJECT 07: SMART PARKING SYSTEM
File: camera.py

Raspberry Pi Camera Module 3 Controller
============================================================
"""

import logging
import time
from datetime import datetime

import cv2
from picamera2 import Picamera2

from config import (
    CAMERA_WIDTH,
    CAMERA_HEIGHT,
    CAMERA_FRAME_RATE,
    CAMERA_ROTATION,
    IMAGE_DIR,
    SAVE_PLATE_IMAGES,
)

logger = logging.getLogger(__name__)


class ParkingCamera:

    def __init__(self):
        self.camera = None
        self.is_running = False

    # --------------------------------------------------------
    # INITIALIZE CAMERA
    # --------------------------------------------------------

    def initialize(self):

        try:
            logger.info("Initializing Camera Module 3...")

            self.camera = Picamera2()

            camera_config = self.camera.create_video_configuration(
                main={
                    "size": (
                        CAMERA_WIDTH,
                        CAMERA_HEIGHT
                    ),
                    "format": "RGB888"
                },
                controls={
                    "FrameRate": CAMERA_FRAME_RATE
                }
            )

            self.camera.configure(camera_config)

            self.camera.start()

            # Allow camera exposure and white balance to settle
            time.sleep(2)

            self.is_running = True

            logger.info("Camera initialized successfully.")

            return True

        except Exception as error:

            logger.exception(
                "Camera initialization failed: %s",
                error
            )

            self.camera = None
            self.is_running = False

            return False

    # --------------------------------------------------------
    # CAPTURE FRAME
    # --------------------------------------------------------

    def capture_frame(self):

        if not self.is_running or self.camera is None:
            logger.error("Camera is not running.")
            return None

        try:

            frame = self.camera.capture_array()

            # Convert RGB image to OpenCV BGR format
            frame = cv2.cvtColor(
                frame,
                cv2.COLOR_RGB2BGR
            )

            # Apply configured rotation
            if CAMERA_ROTATION == 90:
                frame = cv2.rotate(
                    frame,
                    cv2.ROTATE_90_CLOCKWISE
                )

            elif CAMERA_ROTATION == 180:
                frame = cv2.rotate(
                    frame,
                    cv2.ROTATE_180
                )

            elif CAMERA_ROTATION == 270:
                frame = cv2.rotate(
                    frame,
                    cv2.ROTATE_90_COUNTERCLOCKWISE
                )

            return frame

        except Exception as error:

            logger.exception(
                "Frame capture failed: %s",
                error
            )

            return None

    # --------------------------------------------------------
    # CAPTURE AND SAVE VEHICLE IMAGE
    # --------------------------------------------------------

    def capture_vehicle_image(self):

        frame = self.capture_frame()

        if frame is None:
            return None

        if not SAVE_PLATE_IMAGES:
            return frame

        try:

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S_%f"
            )

            filename = f"vehicle_{timestamp}.jpg"

            image_path = IMAGE_DIR / filename

            success = cv2.imwrite(
                str(image_path),
                frame
            )

            if not success:

                logger.error(
                    "Failed to save vehicle image."
                )

                return None

            logger.info(
                "Vehicle image saved: %s",
                image_path
            )

            return str(image_path)

        except Exception as error:

            logger.exception(
                "Vehicle image saving failed: %s",
                error
            )

            return None

    # --------------------------------------------------------
    # CAPTURE MULTIPLE FRAMES
    # --------------------------------------------------------

    def capture_multiple_frames(self, count=5, delay=0.5):

        captured_images = []

        for _ in range(count):

            frame = self.capture_frame()

            if frame is not None:
                captured_images.append(frame)

            time.sleep(delay)

        return captured_images

    # --------------------------------------------------------
    # STOP CAMERA
    # --------------------------------------------------------

    def stop(self):

        if self.camera is not None:

            try:

                self.camera.stop()
                self.camera.close()

                logger.info("Camera stopped successfully.")

            except Exception as error:

                logger.exception(
                    "Camera shutdown failed: %s",
                    error
                )

            finally:

                self.camera = None
                self.is_running = False

    # --------------------------------------------------------
    # CAMERA STATUS
    # --------------------------------------------------------

    def get_status(self):

        return {
            "initialized": self.camera is not None,
            "running": self.is_running,
            "resolution": (
                CAMERA_WIDTH,
                CAMERA_HEIGHT
            )
        }

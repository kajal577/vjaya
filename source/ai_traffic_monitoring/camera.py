
"""
AI TRAFFIC MONITORING SYSTEM
File: camera.py
Description: Camera Module 3 initialization and video capture.
Hardware: Raspberry Pi 5 + Raspberry Pi Camera Module 3
"""

import logging
import time

from picamera2 import Picamera2

from config import CAMERA_SETTINGS


class TrafficCamera:

    def __init__(self):
        self.camera = None
        self.is_running = False

        self.width = CAMERA_SETTINGS["CAMERA_WIDTH"]
        self.height = CAMERA_SETTINGS["CAMERA_HEIGHT"]
        self.frame_rate = CAMERA_SETTINGS["FRAME_RATE"]

        self.logger = logging.getLogger("TrafficCamera")

    # ================================================
    # INITIALIZE CAMERA
    # ================================================

    def initialize(self):

        try:
            self.logger.info("Initializing Raspberry Pi Camera Module 3")

            self.camera = Picamera2()

            camera_config = self.camera.create_video_configuration(
                main={
                    "size": (self.width, self.height),
                    "format": CAMERA_SETTINGS["FORMAT"]
                },
                buffer_count=CAMERA_SETTINGS["BUFFER_COUNT"]
            )

            self.camera.configure(camera_config)

            self.camera.start()

            time.sleep(2)

            self.is_running = True

            self.logger.info("Camera initialized successfully")

            return True

        except Exception as error:

            self.logger.error(
                f"Camera initialization failed: {error}"
            )

            self.release()

            return False

    # ================================================
    # CAPTURE FRAME
    # ================================================

    def capture_frame(self):

        if not self.is_running or self.camera is None:
            self.logger.warning("Camera is not running")
            return None

        try:

            frame = self.camera.capture_array()

            if frame is None:
                self.logger.warning("Empty camera frame received")
                return None

            return frame

        except Exception as error:

            self.logger.error(
                f"Frame capture error: {error}"
            )

            return None

    # ================================================
    # GET CAMERA STATUS
    # ================================================

    def get_status(self):

        return {
            "initialized": self.camera is not None,
            "running": self.is_running,
            "resolution": f"{self.width}x{self.height}",
            "frame_rate": self.frame_rate
        }

    # ================================================
    # STOP CAMERA
    # ================================================

    def stop(self):

        if self.camera is not None and self.is_running:

            try:
                self.camera.stop()
                self.is_running = False

                self.logger.info("Camera stopped")

            except Exception as error:

                self.logger.error(
                    f"Camera stop error: {error}"
                )

    # ================================================
    # RELEASE CAMERA
    # ================================================

    def release(self):

        try:

            if self.camera is not None:

                if self.is_running:
                    self.camera.stop()

                self.camera.close()

                self.camera = None
                self.is_running = False

                self.logger.info("Camera resources released")

        except Exception as error:

            self.logger.error(
                f"Camera release error: {error}"
            )

    # ================================================
    # CONTEXT MANAGER
    # ================================================

    def __enter__(self):

        if not self.initialize():
            raise RuntimeError("Unable to initialize camera")

        return self

    def __exit__(self, exc_type, exc_value, traceback):

        self.release()

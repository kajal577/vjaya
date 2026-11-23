
"""
============================================================
VJaYa Robotics
PROJECT 07: SMART PARKING SYSTEM
File: vehicle_detection.py

Vehicle Detection using OpenCV
============================================================
"""

import cv2
import logging
import time

from camera import ParkingCamera
from config import DUPLICATE_ENTRY_DELAY

logger = logging.getLogger(__name__)


class VehicleDetector:

    def __init__(self, camera=None):

        self.camera = camera or ParkingCamera()

        # Background subtraction for motion detection
        self.background_subtractor = (
            cv2.createBackgroundSubtractorMOG2(
                history=500,
                varThreshold=50,
                detectShadows=True
            )
        )

        # Minimum detected object area
        self.minimum_contour_area = 1500

        # Detection state
        self.vehicle_detected = False
        self.last_detection_time = 0

    # --------------------------------------------------------
    # PREPROCESS FRAME
    # --------------------------------------------------------

    def preprocess_frame(self, frame):

        if frame is None:
            return None

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        blurred = cv2.GaussianBlur(
            gray,
            (5, 5),
            0
        )

        return blurred

    # --------------------------------------------------------
    # DETECT MOVEMENT
    # --------------------------------------------------------

    def detect_motion(self, frame):

        if frame is None:
            return []

        try:

            processed = self.preprocess_frame(frame)

            foreground_mask = (
                self.background_subtractor.apply(
                    processed
                )
            )

            # Remove shadows
            _, threshold = cv2.threshold(
                foreground_mask,
                200,
                255,
                cv2.THRESH_BINARY
            )

            kernel = cv2.getStructuringElement(
                cv2.MORPH_RECT,
                (5, 5)
            )

            threshold = cv2.morphologyEx(
                threshold,
                cv2.MORPH_OPEN,
                kernel
            )

            threshold = cv2.dilate(
                threshold,
                kernel,
                iterations=2
            )

            contours, _ = cv2.findContours(
                threshold,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )

            detected_objects = []

            for contour in contours:

                area = cv2.contourArea(contour)

                if area < self.minimum_contour_area:
                    continue

                x, y, width, height = (
                    cv2.boundingRect(contour)
                )

                detected_objects.append({
                    "x": x,
                    "y": y,
                    "width": width,
                    "height": height,
                    "area": area
                })

            return detected_objects

        except Exception as error:

            logger.exception(
                "Motion detection error: %s",
                error
            )

            return []

    # --------------------------------------------------------
    # CHECK VEHICLE PRESENCE
    # --------------------------------------------------------

    def is_vehicle_present(self, frame):

        detected_objects = self.detect_motion(frame)

        return len(detected_objects) > 0

    # --------------------------------------------------------
    # DETECT VEHICLE AND CAPTURE IMAGE
    # --------------------------------------------------------

    def detect_and_capture(self):

        if not self.camera.is_running:
            logger.warning("Camera is not running.")
            return None

        frame = self.camera.capture_frame()

        if frame is None:
            return None

        detected_objects = self.detect_motion(frame)

        if not detected_objects:
            self.vehicle_detected = False
            return None

        current_time = time.time()

        if (
            current_time - self.last_detection_time
            < DUPLICATE_ENTRY_DELAY
        ):
            return None

        self.last_detection_time = current_time
        self.vehicle_detected = True

        logger.info(
            "Moving object detected in parking area."
        )

        image_path = self.camera.capture_vehicle_image()

        return {
            "detected": True,
            "objects": detected_objects,
            "image_path": image_path,
            "timestamp": current_time
        }

    # --------------------------------------------------------
    # RESET DETECTION
    # --------------------------------------------------------

    def reset_detection(self):

        self.vehicle_detected = False
        self.last_detection_time = 0

        logger.info("Vehicle detection state reset.")

    # --------------------------------------------------------
    # DETECTOR STATUS
    # --------------------------------------------------------

    def get_status(self):

        return {
            "vehicle_detected": self.vehicle_detected,
            "camera_running": self.camera.is_running,
            "minimum_area": self.minimum_contour_area
        }

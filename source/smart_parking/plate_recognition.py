
"""
============================================================
VJaYa Robotics
PROJECT 07: SMART PARKING SYSTEM
File: plate_recognition.py

Automatic Number Plate Recognition (ANPR)
Using Tesseract OCR
============================================================
"""

import re
import logging

import cv2
import pytesseract

from config import (
    OCR_MIN_CONFIDENCE,
    PLATE_PATTERN
)

logger = logging.getLogger(__name__)


class PlateRecognizer:

    def __init__(self):

        self.plate_pattern = re.compile(
            PLATE_PATTERN
        )

        # Tesseract OCR configuration
        self.ocr_config = (
            "--oem 3 --psm 7 "
            "-c tessedit_char_whitelist="
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        )

    # --------------------------------------------------------
    # PREPARE IMAGE
    # --------------------------------------------------------

    def prepare_image(self, image):

        if image is None:
            return None

        try:

            if len(image.shape) == 3:

                image = cv2.cvtColor(
                    image,
                    cv2.COLOR_BGR2GRAY
                )

            # Increase image resolution
            height, width = image.shape[:2]

            image = cv2.resize(
                image,
                (width * 2, height * 2),
                interpolation=cv2.INTER_CUBIC
            )

            # Remove noise
            image = cv2.bilateralFilter(
                image,
                9,
                75,
                75
            )

            # Improve contrast
            image = cv2.equalizeHist(image)

            return image

        except Exception as error:

            logger.exception(
                "OCR image preparation failed: %s",
                error
            )

            return None

    # --------------------------------------------------------
    # EXTRACT TEXT
    # --------------------------------------------------------

    def extract_text(self, image):

        prepared = self.prepare_image(image)

        if prepared is None:
            return ""

        try:

            extracted_text = pytesseract.image_to_string(
                prepared,
                config=self.ocr_config
            )

            return extracted_text

        except Exception as error:

            logger.exception(
                "Tesseract OCR error: %s",
                error
            )

            return ""

    # --------------------------------------------------------
    # CLEAN NUMBER PLATE TEXT
    # --------------------------------------------------------

    def clean_plate_text(self, text):

        if not text:
            return ""

        text = text.upper()

        # Remove spaces, hyphens and special characters
        text = re.sub(
            r"[^A-Z0-9]",
            "",
            text
        )

        return text

    # --------------------------------------------------------
    # VALIDATE INDIAN NUMBER PLATE
    # --------------------------------------------------------

    def validate_plate(self, plate_number):

        if not plate_number:
            return False

        return bool(
            self.plate_pattern.fullmatch(
                plate_number
            )
        )

    # --------------------------------------------------------
    # CALCULATE OCR CONFIDENCE
    # --------------------------------------------------------

    def calculate_confidence(self, image):

        prepared = self.prepare_image(image)

        if prepared is None:
            return 0.0

        try:

            result = pytesseract.image_to_data(
                prepared,
                config=self.ocr_config,
                output_type=pytesseract.Output.DICT
            )

            confidences = []

            for confidence in result["conf"]:

                try:

                    confidence = float(confidence)

                    if confidence >= 0:
                        confidences.append(confidence)

                except (ValueError, TypeError):
                    continue

            if not confidences:
                return 0.0

            return round(
                sum(confidences) / len(confidences),
                2
            )

        except Exception as error:

            logger.exception(
                "OCR confidence calculation failed: %s",
                error
            )

            return 0.0

    # --------------------------------------------------------
    # RECOGNIZE NUMBER PLATE
    # --------------------------------------------------------

    def recognize_plate(self, image):

        try:

            raw_text = self.extract_text(image)

            plate_number = self.clean_plate_text(
                raw_text
            )

            confidence = self.calculate_confidence(
                image
            )

            is_valid = self.validate_plate(
                plate_number
            )

            if not is_valid:

                logger.warning(
                    "Invalid plate detected: %s",
                    plate_number
                )

                return {
                    "success": False,
                    "plate_number": None,
                    "raw_text": raw_text,
                    "confidence": confidence,
                    "valid": False
                }

            if confidence < OCR_MIN_CONFIDENCE:

                logger.warning(
                    "OCR confidence too low: %.2f",
                    confidence
                )

                return {
                    "success": False,
                    "plate_number": plate_number,
                    "raw_text": raw_text,
                    "confidence": confidence,
                    "valid": True
                }

            logger.info(
                "Recognized vehicle: %s",
                plate_number
            )

            return {
                "success": True,
                "plate_number": plate_number,
                "raw_text": raw_text,
                "confidence": confidence,
                "valid": True
            }

        except Exception as error:

            logger.exception(
                "Number plate recognition failed: %s",
                error
            )

            return {
                "success": False,
                "plate_number": None,
                "raw_text": "",
                "confidence": 0.0,
                "valid": False
            }

    # --------------------------------------------------------
    # RECOGNIZE MULTIPLE PLATE CANDIDATES
    # --------------------------------------------------------

    def recognize_multiple(self, plate_candidates):

        results = []

        for candidate in plate_candidates:

            plate_image = candidate.get(
                "processed_image"
            )

            if plate_image is None:
                continue

            result = self.recognize_plate(
                plate_image
            )

            result["candidate_index"] = (
                candidate.get("index")
            )

            results.append(result)

        # Highest confidence first
        results.sort(
            key=lambda item: item["confidence"],
            reverse=True
        )

        return results

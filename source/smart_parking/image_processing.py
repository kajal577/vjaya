
"""
============================================================
VJaYa Robotics
PROJECT 07: SMART PARKING SYSTEM
File: image_processing.py

Vehicle Image Processing and Number Plate Detection
============================================================
"""

import cv2
import logging
import numpy as np

from pathlib import Path

from config import IMAGE_DIR

logger = logging.getLogger(__name__)


class ImageProcessor:

    def __init__(self):

        self.minimum_plate_width = 60
        self.minimum_plate_height = 15

        self.maximum_plate_width = 600
        self.maximum_plate_height = 200

        self.plate_aspect_ratio_min = 2.0
        self.plate_aspect_ratio_max = 6.5

    # --------------------------------------------------------
    # LOAD IMAGE
    # --------------------------------------------------------

    def load_image(self, image_path):

        try:

            image = cv2.imread(str(image_path))

            if image is None:
                logger.error(
                    "Unable to load image: %s",
                    image_path
                )
                return None

            return image

        except Exception as error:

            logger.exception(
                "Image loading error: %s",
                error
            )

            return None

    # --------------------------------------------------------
    # RESIZE IMAGE
    # --------------------------------------------------------

    def resize_image(self, image, width=1280):

        if image is None:
            return None

        height, original_width = image.shape[:2]

        if original_width <= width:
            return image

        ratio = width / original_width

        new_height = int(height * ratio)

        return cv2.resize(
            image,
            (width, new_height),
            interpolation=cv2.INTER_AREA
        )

    # --------------------------------------------------------
    # IMPROVE IMAGE QUALITY
    # --------------------------------------------------------

    def enhance_image(self, image):

        if image is None:
            return None

        try:

            # Convert to LAB color space
            lab = cv2.cvtColor(
                image,
                cv2.COLOR_BGR2LAB
            )

            l_channel, a_channel, b_channel = (
                cv2.split(lab)
            )

            # Improve brightness and contrast
            clahe = cv2.createCLAHE(
                clipLimit=2.0,
                tileGridSize=(8, 8)
            )

            enhanced_l = clahe.apply(l_channel)

            enhanced_lab = cv2.merge([
                enhanced_l,
                a_channel,
                b_channel
            ])

            enhanced = cv2.cvtColor(
                enhanced_lab,
                cv2.COLOR_LAB2BGR
            )

            return enhanced

        except Exception as error:

            logger.exception(
                "Image enhancement error: %s",
                error
            )

            return image

    # --------------------------------------------------------
    # REMOVE IMAGE NOISE
    # --------------------------------------------------------

    def remove_noise(self, image):

        if image is None:
            return None

        return cv2.bilateralFilter(
            image,
            11,
            17,
            17
        )

    # --------------------------------------------------------
    # CONVERT TO GRAYSCALE
    # --------------------------------------------------------

    def convert_to_grayscale(self, image):

        if image is None:
            return None

        return cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

    # --------------------------------------------------------
    # APPLY THRESHOLDING
    # --------------------------------------------------------

    def apply_threshold(self, image):

        if image is None:
            return None

        gray = self.convert_to_grayscale(image)

        gray = cv2.GaussianBlur(
            gray,
            (3, 3),
            0
        )

        threshold = cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            31,
            11
        )

        return threshold

    # --------------------------------------------------------
    # DETECT POSSIBLE NUMBER PLATES
    # --------------------------------------------------------

    def detect_plate_regions(self, image):

        if image is None:
            return []

        try:

            enhanced = self.enhance_image(image)

            filtered = self.remove_noise(enhanced)

            gray = self.convert_to_grayscale(filtered)

            # Edge detection
            edges = cv2.Canny(
                gray,
                50,
                200
            )

            kernel = cv2.getStructuringElement(
                cv2.MORPH_RECT,
                (5, 3)
            )

            edges = cv2.morphologyEx(
                edges,
                cv2.MORPH_CLOSE,
                kernel
            )

            contours, _ = cv2.findContours(
                edges,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )

            plate_regions = []

            for contour in contours:

                x, y, width, height = (
                    cv2.boundingRect(contour)
                )

                if (
                    width < self.minimum_plate_width
                    or height < self.minimum_plate_height
                ):
                    continue

                if (
                    width > self.maximum_plate_width
                    or height > self.maximum_plate_height
                ):
                    continue

                aspect_ratio = width / float(height)

                if not (
                    self.plate_aspect_ratio_min
                    <= aspect_ratio
                    <= self.plate_aspect_ratio_max
                ):
                    continue

                area = width * height

                plate_regions.append({
                    "x": x,
                    "y": y,
                    "width": width,
                    "height": height,
                    "area": area,
                    "aspect_ratio": aspect_ratio
                })

            # Largest candidates first
            plate_regions.sort(
                key=lambda item: item["area"],
                reverse=True
            )

            return plate_regions

        except Exception as error:

            logger.exception(
                "Plate region detection error: %s",
                error
            )

            return []

    # --------------------------------------------------------
    # CROP NUMBER PLATE
    # --------------------------------------------------------

    def crop_plate(self, image, region):

        if image is None or region is None:
            return None

        try:

            x = region["x"]
            y = region["y"]

            width = region["width"]
            height = region["height"]

            plate = image[
                y:y + height,
                x:x + width
            ]

            if plate.size == 0:
                return None

            return plate

        except Exception as error:

            logger.exception(
                "Plate cropping error: %s",
                error
            )

            return None

    # --------------------------------------------------------
    # PREPARE PLATE FOR OCR
    # --------------------------------------------------------

    def prepare_plate_for_ocr(self, plate):

        if plate is None:
            return None

        try:

            # Enlarge plate for OCR
            height, width = plate.shape[:2]

            enlarged = cv2.resize(
                plate,
                (width * 3, height * 3),
                interpolation=cv2.INTER_CUBIC
            )

            enhanced = self.enhance_image(enlarged)

            threshold = self.apply_threshold(enhanced)

            return threshold

        except Exception as error:

            logger.exception(
                "OCR preprocessing error: %s",
                error
            )

            return None

    # --------------------------------------------------------
    # SAVE PROCESSED PLATE
    # --------------------------------------------------------

    def save_plate_image(
        self,
        plate,
        filename="processed_plate.jpg"
    ):

        if plate is None:
            return None

        try:

            output_path = IMAGE_DIR / filename

            success = cv2.imwrite(
                str(output_path),
                plate
            )

            if success:
                logger.info(
                    "Processed plate saved: %s",
                    output_path
                )

                return str(output_path)

            return None

        except Exception as error:

            logger.exception(
                "Processed plate saving error: %s",
                error
            )

            return None

    # --------------------------------------------------------
    # PROCESS VEHICLE IMAGE
    # --------------------------------------------------------

    def process_vehicle_image(self, image_path):

        image = self.load_image(image_path)

        if image is None:
            return []

        image = self.resize_image(image)

        regions = self.detect_plate_regions(image)

        processed_plates = []

        for index, region in enumerate(regions):

            plate = self.crop_plate(
                image,
                region
            )

            if plate is None:
                continue

            prepared = self.prepare_plate_for_ocr(
                plate
            )

            if prepared is None:
                continue

            processed_plates.append({
                "region": region,
                "plate_image": plate,
                "processed_image": prepared,
                "index": index
            })

        return processed_plates

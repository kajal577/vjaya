
"""
============================================================
VJaYa Robotics
PROJECT 07: SMART PARKING SYSTEM
File: logging_config.py

Centralized Logging Configuration
============================================================
"""

import logging
from logging.handlers import RotatingFileHandler

from config import LOG_DIR


# ------------------------------------------------------------
# LOG FILE SETTINGS
# ------------------------------------------------------------

LOG_FILE = LOG_DIR / "smart_parking.log"

LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)s | "
    "%(name)s | "
    "%(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


# ------------------------------------------------------------
# INITIALIZE LOGGING
# ------------------------------------------------------------

def setup_logging(
    log_level=logging.INFO
):

    LOG_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    root_logger = logging.getLogger()

    root_logger.setLevel(log_level)

    # Avoid duplicate handlers when initialized again.
    if getattr(root_logger, "_parking_configured", False):
        return root_logger

    formatter = logging.Formatter(
        LOG_FORMAT,
        datefmt=DATE_FORMAT
    )

    # --------------------------------------------------------
    # FILE HANDLER
    # --------------------------------------------------------

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8"
    )

    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)

    # --------------------------------------------------------
    # CONSOLE HANDLER
    # --------------------------------------------------------

    console_handler = logging.StreamHandler()

    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    # --------------------------------------------------------
    # REGISTER HANDLERS
    # --------------------------------------------------------

    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    root_logger._parking_configured = True

    root_logger.info(
        "Smart Parking logging system initialized."
    )

    return root_logger


# ------------------------------------------------------------
# GET MODULE LOGGER
# ------------------------------------------------------------

def get_logger(name):

    return logging.getLogger(name)


# ------------------------------------------------------------
# LOG VEHICLE ENTRY
# ------------------------------------------------------------

def log_vehicle_entry(
    plate_number,
    parking_slot
):

    logger = get_logger("VehicleEntry")

    logger.info(
        "Vehicle entered | Plate: %s | Slot: %s",
        plate_number,
        parking_slot
    )


# ------------------------------------------------------------
# LOG VEHICLE EXIT
# ------------------------------------------------------------

def log_vehicle_exit(
    plate_number,
    parking_slot,
    parking_fee
):

    logger = get_logger("VehicleExit")

    logger.info(
        "Vehicle exited | Plate: %s | Slot: %s | Fee: Rs.%s",
        plate_number,
        parking_slot,
        parking_fee
    )


# ------------------------------------------------------------
# LOG NUMBER PLATE RECOGNITION
# ------------------------------------------------------------

def log_plate_recognition(
    plate_number,
    confidence,
    valid
):

    logger = get_logger("PlateRecognition")

    logger.info(
        "Plate recognition | Plate: %s | Confidence: %.2f | Valid: %s",
        plate_number,
        confidence,
        valid
    )


# ------------------------------------------------------------
# LOG PARKING SLOT
# ------------------------------------------------------------

def log_slot_allocation(
    plate_number,
    parking_slot
):

    logger = get_logger("ParkingSlot")

    logger.info(
        "Slot allocated | Plate: %s | Slot: %s",
        plate_number,
        parking_slot
    )


# ------------------------------------------------------------
# LOG GATE OPERATION
# ------------------------------------------------------------

def log_gate_operation(
    gate_name,
    operation,
    success
):

    logger = get_logger("Gate")

    logger.info(
        "%s gate | Operation: %s | Success: %s",
        gate_name,
        operation,
        success
    )


# ------------------------------------------------------------
# LOG SYSTEM ERROR
# ------------------------------------------------------------

def log_error(
    message,
    exception=None
):

    logger = get_logger("SystemError")

    if exception:

        logger.exception(
            "%s: %s",
            message,
            exception
        )

    else:

        logger.error(message)


# ------------------------------------------------------------
# LOG SYSTEM EVENT
# ------------------------------------------------------------

def log_event(message):

    logger = get_logger("SystemEvent")

    logger.info(message)

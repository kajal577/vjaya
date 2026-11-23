
"""
AI TRAFFIC MONITORING SYSTEM
File: config.py
Description: Central configuration for the entire project.
Hardware: Raspberry Pi 5 + Hailo AI Accelerator + Camera Module 3
"""

from pathlib import Path
import os

# =====================================================
# PROJECT PATHS
# =====================================================

BASE_DIR = Path(__file__).resolve().parent

MODEL_DIR = BASE_DIR / "models"
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"
UTILS_DIR = BASE_DIR / "utils"

for folder in [MODEL_DIR, DATA_DIR, LOG_DIR, UTILS_DIR]:
    folder.mkdir(parents=True, exist_ok=True)


# =====================================================
# PROJECT INFORMATION
# =====================================================

PROJECT_NAME = "AI Traffic Monitoring System"
PROJECT_VERSION = "1.0.0"

DEBUG_MODE = True


# =====================================================
# HARDWARE CONFIGURATION
# =====================================================

HARDWARE = {
    "PROCESSOR": "Raspberry Pi 5",
    "AI_ACCELERATOR": "Hailo",
    "CAMERA": "Raspberry Pi Camera Module 3"
}


# =====================================================
# CAMERA CONFIGURATION
# =====================================================

CAMERA_SETTINGS = {
    "CAMERA_TYPE": "PICAMERA2",

    "CAMERA_WIDTH": 1280,
    "CAMERA_HEIGHT": 720,

    "FRAME_RATE": 30,

    "FORMAT": "RGB888",

    "FLIP_HORIZONTAL": False,
    "FLIP_VERTICAL": False,

    "BUFFER_COUNT": 4
}


# =====================================================
# HAILO AI MODEL CONFIGURATION
# =====================================================

AI_SETTINGS = {

    # Place your compatible Hailo-compiled HEF model
    # inside the models folder.

    "MODEL_PATH": MODEL_DIR / "vehicle_detection.hef",

    "DEVICE_ID": 0,

    "INPUT_WIDTH": 640,
    "INPUT_HEIGHT": 640,

    "CONFIDENCE_THRESHOLD": 0.50,

    "NMS_THRESHOLD": 0.45,

    "MAX_DETECTIONS": 100,

    "INFERENCE_TIMEOUT": 10
}


# =====================================================
# VEHICLE CLASS CONFIGURATION
# COCO dataset class IDs
# =====================================================

VEHICLE_CLASSES = {
    2: "car",
    3: "motorcycle",
    5: "bus",
    7: "truck"
}

VEHICLE_CLASS_NAMES = list(VEHICLE_CLASSES.values())


# =====================================================
# VEHICLE TRACKING CONFIGURATION
# =====================================================

TRACKING_SETTINGS = {

    "TRACKER_TYPE": "CENTROID",

    "MAX_DISAPPEARED": 30,

    "MAX_DISTANCE": 80,

    "MIN_TRACKING_FRAMES": 3,

    "SHOW_TRACKING_ID": True,

    "SHOW_TRACKING_PATH": True
}


# =====================================================
# VEHICLE COUNTING CONFIGURATION
# =====================================================

COUNTING_SETTINGS = {

    "ENABLE_COUNTING": True,

    # Horizontal counting line position
    # Expressed as a fraction of frame height.

    "COUNTING_LINE_POSITION": 0.50,

    "COUNTING_LINE_COLOR": (0, 255, 0),

    "COUNTING_LINE_THICKNESS": 2,

    "COUNTING_DIRECTION": "BOTH",

    "PREVENT_DUPLICATE_COUNT": True
}


# =====================================================
# TRAFFIC ANALYSIS CONFIGURATION
# =====================================================

TRAFFIC_SETTINGS = {

    "ANALYSIS_INTERVAL": 5,

    "LOW_TRAFFIC_MAX": 5,

    "MEDIUM_TRAFFIC_MAX": 15,

    "HIGH_TRAFFIC_MAX": 30,

    "ENABLE_STATISTICS": True
}


# =====================================================
# CONGESTION DETECTION CONFIGURATION
# =====================================================

CONGESTION_SETTINGS = {

    "LOW": 5,

    "MEDIUM": 15,

    "HIGH": 30,

    "SEVERE": 45,

    "UPDATE_INTERVAL": 5
}


# =====================================================
# DATABASE CONFIGURATION
# =====================================================

DATABASE_SETTINGS = {

    "DATABASE_TYPE": "SQLITE",

    "DATABASE_PATH": DATA_DIR / "traffic_data.db",

    "SAVE_VEHICLE_RECORDS": True,

    "SAVE_TRAFFIC_STATISTICS": True
}


# =====================================================
# DASHBOARD CONFIGURATION
# =====================================================

DASHBOARD_SETTINGS = {

    "HOST": "0.0.0.0",

    "PORT": 5000,

    "DEBUG": False,

    "ENABLE_LIVE_VIDEO": True,

    "ENABLE_VEHICLE_STATISTICS": True,

    "ENABLE_CONGESTION_STATUS": True
}


# =====================================================
# LOGGING CONFIGURATION
# =====================================================

LOG_SETTINGS = {

    "LOG_FILE": LOG_DIR / "traffic_monitor.log",

    "LOG_LEVEL": "INFO",

    "LOG_FORMAT": (
        "%(asctime)s - %(levelname)s - %(message)s"
    )
}


# =====================================================
# DISPLAY CONFIGURATION
# =====================================================

DISPLAY_SETTINGS = {

    "WINDOW_NAME": "AI Traffic Monitoring System",

    "SHOW_WINDOW": True,

    "SHOW_FPS": True,

    "SHOW_VEHICLE_COUNT": True,

    "SHOW_CONGESTION": True,

    "SHOW_CLASS_LABELS": True
}


# =====================================================
# ENVIRONMENT OVERRIDES
# =====================================================

CAMERA_WIDTH = int(
    os.getenv("CAMERA_WIDTH", CAMERA_SETTINGS["CAMERA_WIDTH"])
)

CAMERA_HEIGHT = int(
    os.getenv("CAMERA_HEIGHT", CAMERA_SETTINGS["CAMERA_HEIGHT"])
)

CONFIDENCE_THRESHOLD = float(
    os.getenv(
        "CONFIDENCE_THRESHOLD",
        AI_SETTINGS["CONFIDENCE_THRESHOLD"]
    )
)

print(f"{PROJECT_NAME} configuration loaded.")

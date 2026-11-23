
# ============================================================
# VJaYa Robotics
# PROJECT 07: SMART PARKING SYSTEM
# File: config.py
# Hardware: Raspberry Pi 5 + Camera Module 3
# ============================================================

from pathlib import Path

# ---------------- PROJECT SETTINGS ----------------

PROJECT_NAME = "VJaYa Smart Parking System"
PROJECT_VERSION = "1.0.0"

# Project directory
BASE_DIR = Path(__file__).resolve().parent

# ---------------- DIRECTORY SETTINGS ----------------

DATABASE_DIR = BASE_DIR / "database"
IMAGE_DIR = BASE_DIR / "captured_images"
LOG_DIR = BASE_DIR / "logs"

DATABASE_PATH = DATABASE_DIR / "parking.db"

# Create required directories
for directory in (DATABASE_DIR, IMAGE_DIR, LOG_DIR):
    directory.mkdir(parents=True, exist_ok=True)

# ---------------- RASPBERRY PI GPIO ----------------

# BCM GPIO numbering
GPIO_MODE = "BCM"

# Servo motor for entrance barrier
ENTRY_SERVO_PIN = 18

# Servo motor for exit barrier
EXIT_SERVO_PIN = 19

# Entrance vehicle detection sensor
ENTRY_SENSOR_PIN = 23

# Exit vehicle detection sensor
EXIT_SENSOR_PIN = 24

# Parking slot sensors
PARKING_SENSOR_PINS = {
    1: 5,
    2: 6,
    3: 12,
    4: 13,
}

# ---------------- SERVO SETTINGS ----------------

GATE_CLOSED_ANGLE = 0
GATE_OPEN_ANGLE = 90

GATE_OPEN_DURATION = 5

# ---------------- CAMERA SETTINGS ----------------

CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720

CAMERA_FRAME_RATE = 30

CAMERA_ROTATION = 0

# Number plate image storage
SAVE_PLATE_IMAGES = True

# ---------------- PARKING SETTINGS ----------------

TOTAL_PARKING_SLOTS = 4

PARKING_SLOT_NAMES = [
    "P1",
    "P2",
    "P3",
    "P4",
]

# ---------------- NUMBER PLATE RECOGNITION ----------------

# Minimum OCR confidence (percentage)
OCR_MIN_CONFIDENCE = 60

# Indian vehicle registration format
# Example: BR01AB1234
PLATE_PATTERN = (
    r"^[A-Z]{2}[0-9]{1,2}"
    r"[A-Z]{1,3}[0-9]{1,4}$"
)

# ---------------- PARKING FEE SETTINGS ----------------

# Fee per hour in INR
PARKING_FEE_PER_HOUR = 20

# Minimum parking fee
MINIMUM_PARKING_FEE = 20

# ---------------- SYSTEM SETTINGS ----------------

DEBUG_MODE = True

LOG_FILE = LOG_DIR / "parking_system.log"

# Duplicate vehicle detection delay
DUPLICATE_ENTRY_DELAY = 10

# Sensor polling interval
SENSOR_POLL_INTERVAL = 0.2

# ---------------- DISPLAY SETTINGS ----------------

LCD_ENABLED = True

LCD_ADDRESS = 0x27

LCD_COLUMNS = 16
LCD_ROWS = 2

# ---------------- SECURITY SETTINGS ----------------

ALLOW_UNKNOWN_VEHICLES = False

REQUIRE_VALID_NUMBER_PLATE = True


"""
VJaYa Robotics
Project 14: AI Face Recognition Door Access System

Central configuration file for Raspberry Pi 5.
"""

from pathlib import Path

# ==================================================
# PROJECT PATHS
# ==================================================

BASE_DIR = Path(__file__).resolve().parent

REGISTERED_FACES_DIR = BASE_DIR / "registered_faces"

DATABASE_DIR = BASE_DIR / "database"

ACCESS_DATABASE = DATABASE_DIR / "access_logs.db"


# ==================================================
# RASPBERRY PI GPIO CONFIGURATION
# BCM GPIO numbering
# ==================================================

# Relay controlling the 5V demonstration solenoid lock
LOCK_RELAY_PIN = 17

# Physical manual override push button
MANUAL_OVERRIDE_PIN = 27

# Optional buzzer
BUZZER_PIN = 22


# ==================================================
# DOOR LOCK SETTINGS
# ==================================================

# Common relay modules are active LOW.
# Verify your actual relay module before enabling it.

LOCK_RELAY_ACTIVE_LOW = True

# Lock remains unlocked for this duration.
UNLOCK_DURATION = 3

# Start with the lock output inactive.
LOCK_DEFAULT_STATE = "LOCKED"


# ==================================================
# CAMERA CONFIGURATION
# ==================================================

CAMERA_WIDTH = 1280

CAMERA_HEIGHT = 720

CAMERA_CHANNELS = 3

CAMERA_FLIP = False

CAMERA_FRAME_RATE = 30


# ==================================================
# FACE RECOGNITION SETTINGS
# ==================================================

# Recognition confidence threshold.
# This value will be calibrated with the selected
# face recognition model.

FACE_MATCH_THRESHOLD = 0.50

# Minimum face size for processing.
MIN_FACE_SIZE = 40

# Number of consecutive recognition frames
# required before granting access.

REQUIRED_MATCH_FRAMES = 3


# ==================================================
# SECURITY SETTINGS
# ==================================================

# Unknown faces are denied access.
ALLOW_UNKNOWN_FACES = False

# Prevent repeated access attempts.
ACCESS_COOLDOWN = 5

# Save access events in the database.
ENABLE_ACCESS_LOGGING = True


# ==================================================
# BUZZER SETTINGS
# ==================================================

BUZZER_ENABLED = True

ACCESS_GRANTED_BEEP = 0.15

ACCESS_DENIED_BEEP = 0.50


# ==================================================
# DISPLAY SETTINGS
# ==================================================

DISPLAY_ENABLED = False


# ==================================================
# APPLICATION SETTINGS
# ==================================================

APPLICATION_NAME = "VJaYa AI Door Access System"

DEBUG_MODE = True


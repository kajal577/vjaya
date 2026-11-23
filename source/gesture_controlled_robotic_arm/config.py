
"""
GESTURE CONTROLLED ROBOTIC ARM
File: config.py

Project configuration for Raspberry Pi 5.
Supports 4-DOF and 5-DOF robotic arms.
"""

# ==============================
# ROBOT ARM CONFIGURATION
# ==============================

# Set to 4 or 5 depending on your robotic arm.
DOF = 5

# PCA9685 I2C address
PCA9685_ADDRESS = 0x40

# Servo driver frequency
SERVO_FREQUENCY = 50

# Servo channels on PCA9685
# Base, shoulder, elbow, wrist, gripper
SERVO_CHANNELS = {
    "base": 0,
    "shoulder": 1,
    "elbow": 2,
    "wrist": 3,
    "gripper": 4,
}

# ==============================
# SERVO ANGLE LIMITS
# ==============================

SERVO_LIMITS = {
    "base": (0, 180),
    "shoulder": (20, 160),
    "elbow": (20, 160),
    "wrist": (0, 180),
    "gripper": (20, 100),
}

# Initial servo positions
SERVO_HOME = {
    "base": 90,
    "shoulder": 90,
    "elbow": 90,
    "wrist": 90,
    "gripper": 60,
}

# ==============================
# CAMERA CONFIGURATION
# ==============================

# USB webcam: usually 0
# Raspberry Pi Camera: configure separately
CAMERA_INDEX = 0

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_FPS = 30

# ==============================
# HAND TRACKING
# ==============================

HAND_DETECTION_CONFIDENCE = 0.7
HAND_TRACKING_CONFIDENCE = 0.7

# Movement smoothing
SMOOTHING_FACTOR = 0.25

# ==============================
# CONTROL CONFIGURATION
# ==============================

# Maximum servo movement per control update
MAX_SERVO_STEP = 3

# Enable/disable mirror view
MIRROR_CAMERA = True

# Keyboard emergency stop
EMERGENCY_STOP_KEY = "q"

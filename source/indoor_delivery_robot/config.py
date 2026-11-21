
"""
INDOOR DELIVERY ROBOT
VJaYa Robotics

File: config.py
Controller: Raspberry Pi 5
"""

# ==========================================
# RASPBERRY PI CONFIGURATION
# ==========================================

ROBOT_NAME = "VJaYa Indoor Delivery Robot"

GPIO_MODE = "BCM"


# ==========================================
# TB6612FNG MOTOR DRIVER
# ==========================================

# Left motor group - Channel A
MOTOR_LEFT_IN1 = 17
MOTOR_LEFT_IN2 = 27
MOTOR_LEFT_PWM = 18

# Right motor group - Channel B
MOTOR_RIGHT_IN1 = 22
MOTOR_RIGHT_IN2 = 23
MOTOR_RIGHT_PWM = 13

# Motor driver standby pin
MOTOR_STBY = 24

# Motor speed settings
MOTOR_SPEED = 50
MAX_MOTOR_SPEED = 100
MIN_MOTOR_SPEED = 0


# ==========================================
# DISTANCE SENSOR CONFIGURATION
# ==========================================

# VL53L0X I2C sensor
I2C_SDA = 2
I2C_SCL = 3

# Obstacle detection distance (centimeters)
OBSTACLE_DISTANCE = 25

# Emergency stopping distance (centimeters)
EMERGENCY_DISTANCE = 12


# ==========================================
# WHEEL ENCODER CONFIGURATION
# ==========================================

# Left wheel encoder
ENCODER_LEFT_A = 5
ENCODER_LEFT_B = 6

# Right wheel encoder
ENCODER_RIGHT_A = 16
ENCODER_RIGHT_B = 20

# Encoder calibration
ENCODER_PPR = 20

# Wheel dimensions (millimeters)
WHEEL_DIAMETER = 65

# Distance between left and right wheel centers (mm)
WHEEL_BASE = 180


# ==========================================
# NAVIGATION CONFIGURATION
# ==========================================

# Default robot movement speed
NAVIGATION_SPEED = 40

# Navigation update interval (seconds)
NAVIGATION_INTERVAL = 0.1

# Maximum allowed navigation error (mm)
POSITION_TOLERANCE = 30

# Default turning angle
TURN_ANGLE = 90


# ==========================================
# DELIVERY CONFIGURATION
# ==========================================

# Available delivery locations
DELIVERY_LOCATIONS = {
    "ROOM_1": (1000, 0),
    "ROOM_2": (2000, 0),
    "ROOM_3": (2000, 1000),
    "HOME": (0, 0)
}

# Default delivery destination
DEFAULT_DESTINATION = "ROOM_1"


# ==========================================
# WEB DASHBOARD CONFIGURATION
# ==========================================

WEB_HOST = "0.0.0.0"
WEB_PORT = 5000

DEBUG_MODE = False


# ==========================================
# SAFETY CONFIGURATION
# ==========================================

# Stop motors if an obstacle is detected
OBSTACLE_STOP_ENABLED = True

# Maximum delivery movement duration (seconds)
MAX_DELIVERY_TIME = 300

# Robot startup motor state
MOTORS_ENABLED_AT_STARTUP = False


# ==========================================
# BATTERY MONITORING
# ==========================================

BATTERY_WARNING_PERCENT = 20
BATTERY_CRITICAL_PERCENT = 10


print("Indoor Delivery Robot Configuration Loaded")


"""
AUTONOMOUS ROBOT VACUUM
File: robot_config.py

Central configuration for Raspberry Pi 5 robot.
VJaYa Robotics
"""

# ==========================================
# ROBOT INFORMATION
# ==========================================

ROBOT_NAME = "AUTONOMOUS_ROBOT_VACUUM"
ROBOT_VERSION = "1.0.0"

# ==========================================
# ROS 2 CONFIGURATION
# ==========================================

ROS_DISTRO = "jazzy"

BASE_FRAME = "base_link"
ODOM_FRAME = "odom"
MAP_FRAME = "map"
LIDAR_FRAME = "laser_frame"
IMU_FRAME = "imu_link"

# ==========================================
# ROBOT DIMENSIONS
# ==========================================

# These are initial example values.
# Measure your actual chassis before calibration.

WHEEL_RADIUS = 0.035       # meters
WHEEL_SEPARATION = 0.22    # meters

ROBOT_LENGTH = 0.30        # meters
ROBOT_WIDTH = 0.26         # meters
ROBOT_HEIGHT = 0.12        # meters

# ==========================================
# MOTOR CONFIGURATION
# ==========================================

MOTOR_COUNT = 2

LEFT_MOTOR_NAME = "left_motor"
RIGHT_MOTOR_NAME = "right_motor"

MOTOR_MAX_SPEED = 0.30     # meters/second
MOTOR_MIN_SPEED = 0.05     # meters/second

# Motor GPIO pins must be configured
# according to the actual motor driver.

LEFT_MOTOR_GPIO = None
RIGHT_MOTOR_GPIO = None

# ==========================================
# ENCODER CONFIGURATION
# ==========================================

ENCODER_ENABLED = True

LEFT_ENCODER_GPIO_A = None
LEFT_ENCODER_GPIO_B = None

RIGHT_ENCODER_GPIO_A = None
RIGHT_ENCODER_GPIO_B = None

ENCODER_TICKS_PER_REVOLUTION = None

# ==========================================
# LIDAR CONFIGURATION
# ==========================================

LIDAR_ENABLED = True

LIDAR_PORT = "/dev/ttyUSB0"
LIDAR_BAUDRATE = None

LIDAR_FRAME = "laser_frame"

LIDAR_SCAN_TOPIC = "/scan"

LIDAR_MIN_RANGE = 0.12
LIDAR_MAX_RANGE = 8.0

# Set baud rate and driver according
# to the exact LiDAR model.

# ==========================================
# IMU CONFIGURATION
# ==========================================

IMU_ENABLED = True

IMU_I2C_ADDRESS = 0x68
IMU_FRAME = "imu_link"

IMU_TOPIC = "/imu/data"

# Confirm the actual IMU model and address
# before enabling its driver.

# ==========================================
# ULTRASONIC CONFIGURATION
# ==========================================

ULTRASONIC_ENABLED = True

ULTRASONIC_COUNT = 2

ULTRASONIC_FRONT_GPIO_TRIGGER = None
ULTRASONIC_FRONT_GPIO_ECHO = None

ULTRASONIC_REAR_GPIO_TRIGGER = None
ULTRASONIC_REAR_GPIO_ECHO = None

# ==========================================
# BUMPER CONFIGURATION
# ==========================================

BUMPER_ENABLED = True

BUMPER_FRONT_GPIO = None
BUMPER_REAR_GPIO = None

# ==========================================
# CLEANING SYSTEM
# ==========================================

VACUUM_ENABLED = False
BRUSH_ENABLED = False

VACUUM_GPIO = None
BRUSH_GPIO = None

# Cleaning hardware remains disabled
# until its power circuits are installed
# and independently tested.

# ==========================================
# NAVIGATION CONFIGURATION
# ==========================================

LINEAR_SPEED_LIMIT = 0.30
ANGULAR_SPEED_LIMIT = 1.0

OBSTACLE_STOP_DISTANCE = 0.25

NAVIGATION_ENABLED = True
SLAM_ENABLED = True

# ==========================================
# SAFETY CONFIGURATION
# ==========================================

EMERGENCY_STOP_ENABLED = True

MOTOR_STARTUP_DELAY = 2.0

STOP_ON_SENSOR_FAILURE = True
STOP_ON_LIDAR_FAILURE = True

# ==========================================
# BATTERY CONFIGURATION
# ==========================================

BATTERY_MONITOR_ENABLED = False

LOW_BATTERY_PERCENTAGE = 20

# ==========================================
# DEBUG CONFIGURATION
# ==========================================

DEBUG_MODE = True

LOG_LEVEL = "INFO"

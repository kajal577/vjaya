"""Hardware settings for Indoor Mapping Robot. BCM GPIO numbering."""
LEFT_IN1 = 17
LEFT_IN2 = 27
LEFT_EN = 18
RIGHT_IN1 = 22
RIGHT_IN2 = 23
RIGHT_EN = 13
LEFT_ENCODER_A = 24
RIGHT_ENCODER_A = 25

# Measure and update for your wheel/encoder assembly.
WHEEL_DIAMETER_M = 0.065
WHEEL_BASE_M = 0.150
ENCODER_COUNTS_PER_WHEEL_REV = 360.0  # effective counts after your encoder gearing
MAX_LINEAR_MPS = 0.25
MAX_ANGULAR_RPS = 1.2
PWM_FREQUENCY_HZ = 1000

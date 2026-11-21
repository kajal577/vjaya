"""Raspberry Pi Robot Dog settings. Calibrate servo centers and directions before use."""
PCA9685_ADDRESS = 0x40
SERVO_PWM_HZ = 50
SERVO_MIN_PULSE_US = 500
SERVO_MAX_PULSE_US = 2500
SERVO_CHANNELS = {
    # Each leg: hip yaw, shoulder, knee. Change channel assignments to match wiring.
    'front_left':  (0, 1, 2),
    'front_right': (3, 4, 5),
    'rear_left':   (6, 7, 8),
    'rear_right':  (9, 10, 11),
}
# Per-channel neutral angle and direction. Adjust after checking each servo horn.
SERVO_CENTER_DEG = [90] * 12
SERVO_REVERSE = [False, False, False, False, True, True,
                 False, False, False, False, True, True]
SERVO_MIN_DEG = 25
SERVO_MAX_DEG = 155

# HC-SR04: ECHO must be reduced to 3.3 V with a resistor divider/level shifter.
ULTRASONIC_TRIGGER_BCM = 20
ULTRASONIC_ECHO_BCM = 21
OBSTACLE_STOP_CM = 22.0

WALK_STEP_SECONDS = 0.65
WALK_SWING_DEG = 18.0
KNEE_BEND_DEG = 22.0


"""
INDOOR DELIVERY ROBOT
VJaYa Robotics

File: motor_control.py
Controller: Raspberry Pi 5
Motor Driver: TB6612FNG

Functions:
    init_motors()
    move_forward()
    move_backward()
    turn_left()
    turn_right()
    set_speed()
    stop_motors()
    cleanup_motors()
"""

from gpiozero import DigitalOutputDevice
from gpiozero import PWMOutputDevice

import config


# ==========================================
# MOTOR OBJECTS
# ==========================================

left_in1 = None
left_in2 = None
left_pwm = None

right_in1 = None
right_in2 = None
right_pwm = None

standby = None

motors_initialized = False

current_speed = config.MOTOR_SPEED


# ==========================================
# INITIALIZE MOTORS
# ==========================================

def init_motors():
    """
    Initialize TB6612FNG motor driver.

    Motors remain stopped during initialization.
    """

    global left_in1
    global left_in2
    global left_pwm

    global right_in1
    global right_in2
    global right_pwm

    global standby
    global motors_initialized

    if motors_initialized:
        return

    try:
        # Left motor direction
        left_in1 = DigitalOutputDevice(
            config.MOTOR_LEFT_IN1,
            initial_value=False
        )

        left_in2 = DigitalOutputDevice(
            config.MOTOR_LEFT_IN2,
            initial_value=False
        )

        # Left motor speed
        left_pwm = PWMOutputDevice(
            config.MOTOR_LEFT_PWM,
            frequency=1000,
            initial_value=0
        )

        # Right motor direction
        right_in1 = DigitalOutputDevice(
            config.MOTOR_RIGHT_IN1,
            initial_value=False
        )

        right_in2 = DigitalOutputDevice(
            config.MOTOR_RIGHT_IN2,
            initial_value=False
        )

        # Right motor speed
        right_pwm = PWMOutputDevice(
            config.MOTOR_RIGHT_PWM,
            frequency=1000,
            initial_value=0
        )

        # Motor driver standby
        standby = DigitalOutputDevice(
            config.MOTOR_STBY,
            initial_value=False
        )

        # Keep driver disabled at startup
        standby.off()

        motors_initialized = True

        print("Motor Control Initialized")
        print("TB6612FNG is in standby mode")

    except Exception as error:
        print("Motor initialization failed:", error)

        cleanup_motors()

        raise


# ==========================================
# CHECK INITIALIZATION
# ==========================================

def _check_initialized():
    """
    Check whether motor control is initialized.
    """

    if not motors_initialized:
        raise RuntimeError(
            "Motors are not initialized. "
            "Call init_motors() first."
        )


# ==========================================
# ENABLE MOTOR DRIVER
# ==========================================

def _enable_driver():
    """
    Enable TB6612FNG motor driver.
    """

    _check_initialized()

    standby.on()


# ==========================================
# SET MOTOR SPEED
# ==========================================

def set_speed(speed):
    """
    Set motor speed from 0 to 100 percent.

    Example:
        set_speed(50)
    """

    global current_speed

    speed = max(
        config.MIN_MOTOR_SPEED,
        min(config.MAX_MOTOR_SPEED, speed)
    )

    current_speed = speed

    if motors_initialized:
        left_pwm.value = speed / 100.0
        right_pwm.value = speed / 100.0

    print("Motor speed:", speed, "%")


# ==========================================
# LEFT MOTOR CONTROL
# ==========================================

def _left_forward():
    """
    Rotate left motor group forward.
    """

    left_in1.on()
    left_in2.off()


def _left_backward():
    """
    Rotate left motor group backward.
    """

    left_in1.off()
    left_in2.on()


def _left_stop():
    """
    Stop left motor group.
    """

    left_pwm.value = 0

    left_in1.off()
    left_in2.off()


# ==========================================
# RIGHT MOTOR CONTROL
# ==========================================

def _right_forward():
    """
    Rotate right motor group forward.
    """

    right_in1.on()
    right_in2.off()


def _right_backward():
    """
    Rotate right motor group backward.
    """

    right_in1.off()
    right_in2.on()


def _right_stop():
    """
    Stop right motor group.
    """

    right_pwm.value = 0

    right_in1.off()
    right_in2.off()


# ==========================================
# MOVE FORWARD
# ==========================================

def move_forward(speed=None):
    """
    Move robot forward.

    Example:
        move_forward()
        move_forward(60)
    """

    _enable_driver()

    if speed is not None:
        set_speed(speed)

    _left_forward()
    _right_forward()

    left_pwm.value = current_speed / 100.0
    right_pwm.value = current_speed / 100.0

    print("Robot moving forward")


# ==========================================
# MOVE BACKWARD
# ==========================================

def move_backward(speed=None):
    """
    Move robot backward.
    """

    _enable_driver()

    if speed is not None:
        set_speed(speed)

    _left_backward()
    _right_backward()

    left_pwm.value = current_speed / 100.0
    right_pwm.value = current_speed / 100.0

    print("Robot moving backward")


# ==========================================
# TURN LEFT
# ==========================================

def turn_left(speed=None):
    """
    Rotate robot left.

    Left motor backward.
    Right motor forward.
    """

    _enable_driver()

    if speed is not None:
        set_speed(speed)

    _left_backward()
    _right_forward()

    left_pwm.value = current_speed / 100.0
    right_pwm.value = current_speed / 100.0

    print("Robot turning left")


# ==========================================
# TURN RIGHT
# ==========================================

def turn_right(speed=None):
    """
    Rotate robot right.

    Left motor forward.
    Right motor backward.
    """

    _enable_driver()

    if speed is not None:
        set_speed(speed)

    _left_forward()
    _right_backward()

    left_pwm.value = current_speed / 100.0
    right_pwm.value = current_speed / 100.0

    print("Robot turning right")


# ==========================================
# STOP MOTORS
# ==========================================

def stop_motors():
    """
    Stop both motor groups.

    Also disables the TB6612FNG driver.
    """

    if not motors_initialized:
        return

    _left_stop()
    _right_stop()

    standby.off()

    print("Robot stopped")


# ==========================================
# CLEANUP MOTORS
# ==========================================

def cleanup_motors():
    """
    Stop motors and release GPIO resources.
    """

    global motors_initialized

    if not motors_initialized:
        return

    try:
        stop_motors()

    except Exception:
        pass

    devices = [
        left_in1,
        left_in2,
        left_pwm,
        right_in1,
        right_in2,
        right_pwm,
        standby
    ]

    for device in devices:
        if device is not None:
            try:
                device.close()
            except Exception:
                pass

    motors_initialized = False

    print("Motor GPIO resources released")


# ==========================================
# TEST FUNCTION
# ==========================================

def test_motors():
    """
    Basic motor test.

    Test only with robot wheels raised.
    """

    print("Starting motor test")

    init_motors()

    try:
        move_forward(30)
        input("Press Enter to stop forward movement...")

        stop_motors()

        move_backward(30)
        input("Press Enter to stop backward movement...")

        stop_motors()

        turn_left(30)
        input("Press Enter to stop left turn...")

        stop_motors()

        turn_right(30)
        input("Press Enter to stop right turn...")

        stop_motors()

    finally:
        cleanup_motors()

    print("Motor test completed")

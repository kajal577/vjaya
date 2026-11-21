
"""
INDOOR DELIVERY ROBOT
File: navigation.py

Basic movement, encoder distance control,
and obstacle-aware navigation.
"""

import time

import config
import motor_control
import sensors
import encoder


_navigation_initialized = False


def init_navigation():
    """
    Initialize motors, distance sensor, and wheel encoders.
    """
    global _navigation_initialized

    try:
        motor_control.init_motors()

        sensor_ok = sensors.init_sensors()
        encoder_ok = encoder.init_encoders()

        if not sensor_ok or not encoder_ok:
            motor_control.stop_motors()
            _navigation_initialized = False

            print("Navigation initialization failed.")
            return False

        encoder.reset_encoder_counts()

        _navigation_initialized = True

        print("Navigation initialized.")
        return True

    except Exception as error:
        motor_control.stop_motors()
        _navigation_initialized = False

        print(f"Navigation initialization error: {error}")
        return False


def _check_initialized():
    """
    Ensure navigation has been initialized.
    """
    if not _navigation_initialized:
        raise RuntimeError(
            "Navigation is not initialized. "
            "Call init_navigation() first."
        )


def stop():
    """
    Stop both motors immediately.
    """
    motor_control.stop_motors()


def move_forward():
    """
    Move forward continuously.
    Stops if an obstacle is detected.
    """
    _check_initialized()

    if sensors.obstacle_detected():
        stop()
        print("Obstacle detected. Robot stopped.")
        return False

    motor_control.set_speed(config.NAVIGATION_SPEED)
    motor_control.move_forward()

    return True


def move_backward():
    """
    Move backward continuously.
    """
    _check_initialized()

    motor_control.set_speed(config.NAVIGATION_SPEED)
    motor_control.move_backward()

    return True


def turn_left():
    """
    Turn left in place.
    """
    _check_initialized()

    motor_control.set_speed(config.NAVIGATION_SPEED)
    motor_control.turn_left()


def turn_right():
    """
    Turn right in place.
    """
    _check_initialized()

    motor_control.set_speed(config.NAVIGATION_SPEED)
    motor_control.turn_right()


def move_distance_cm(distance_cm, speed=None):
    """
    Move forward a specified distance using wheel encoders.

    Returns:
        True if the target distance is reached.
        False if an obstacle or error stops the movement.
    """
    _check_initialized()

    if distance_cm <= 0:
        print("Distance must be greater than zero.")
        return False

    if speed is None:
        speed = config.NAVIGATION_SPEED

    encoder.reset_encoder_counts()

    motor_control.set_speed(speed)

    start_time = time.monotonic()
    timeout_seconds = 30.0

    try:
        motor_control.move_forward()

        while True:
            distance_travelled = encoder.get_average_distance_cm()

            if distance_travelled >= distance_cm:
                stop()
                print(f"Target reached: {distance_travelled:.1f} cm")
                return True

            if sensors.obstacle_detected():
                stop()
                print("Obstacle detected. Movement cancelled.")
                return False

            if time.monotonic() - start_time > timeout_seconds:
                stop()
                print("Movement timeout.")
                return False

            time.sleep(config.NAVIGATION_INTERVAL)

    except Exception as error:
        stop()
        print(f"Distance movement error: {error}")
        return False

    finally:
        stop()


def rotate_degrees(angle, speed=None):
    """
    Rotate the robot in place by an approximate angle.

    Positive angle = turn right.
    Negative angle = turn left.

    Uses wheel encoder distance and configured wheel base.
    """
    _check_initialized()

    if angle == 0:
        return True

    if speed is None:
        speed = config.NAVIGATION_SPEED

    # Each wheel travels half the distance around
    # the robot's turning circle.
    wheel_distance_mm = (
        3.141592653589793
        * config.WHEEL_BASE_MM
        * abs(angle)
        / 360.0
    )

    target_distance_cm = wheel_distance_mm / 10.0

    encoder.reset_encoder_counts()
    motor_control.set_speed(speed)

    start_time = time.monotonic()
    timeout_seconds = 20.0

    try:
        if angle > 0:
            motor_control.turn_right()
        else:
            motor_control.turn_left()

        while True:
            left_distance = abs(
                encoder.get_left_distance_mm()
            )

            right_distance = abs(
                encoder.get_right_distance_mm()
            )

            average_distance_cm = (
                left_distance + right_distance
            ) / 20.0

            if average_distance_cm >= target_distance_cm:
                stop()
                print(f"Rotation complete: {angle} degrees")
                return True

            if sensors.emergency_obstacle_detected():
                stop()
                print("Emergency obstacle stop.")
                return False

            if time.monotonic() - start_time > timeout_seconds:
                stop()
                print("Rotation timeout.")
                return False

            time.sleep(config.NAVIGATION_INTERVAL)

    except Exception as error:
        stop()
        print(f"Rotation error: {error}")
        return False

    finally:
        stop()


def turn_left_90():
    """
    Turn left approximately 90 degrees.
    """
    return rotate_degrees(-90)


def turn_right_90():
    """
    Turn right approximately 90 degrees.
    """
    return rotate_degrees(90)


def cleanup_navigation():
    """
    Stop the robot and release all hardware resources.
    """
    global _navigation_initialized

    stop()

    try:
        encoder.cleanup_encoders()
    except Exception as error:
        print(f"Encoder cleanup error: {error}")

    try:
        sensors.cleanup_sensors()
    except Exception as error:
        print(f"Sensor cleanup error: {error}")

    try:
        motor_control.cleanup_motors()
    except Exception as error:
        print(f"Motor cleanup error: {error}")

    _navigation_initialized = False

    print("Navigation cleanup complete.")


def test_navigation():
    """
    Basic navigation test.
    Keep the robot wheels lifted during initial testing.
    """
    if not init_navigation():
        print("Navigation test cannot start.")
        return

    try:
        print("Moving forward 20 cm...")
        move_distance_cm(20)

        time.sleep(1)

        print("Turning right 90 degrees...")
        turn_right_90()

        time.sleep(1)

        print("Moving forward 20 cm...")
        move_distance_cm(20)

    except KeyboardInterrupt:
        print("Navigation test interrupted.")

    finally:
        cleanup_navigation()


if __name__ == "__main__":
    test_navigation()

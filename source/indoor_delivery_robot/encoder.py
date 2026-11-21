
"""
INDOOR DELIVERY ROBOT
File: encoder.py

Wheel encoder reading and distance calculation.
"""

from gpiozero import RotaryEncoder

import config


_left_encoder = None
_right_encoder = None
_encoders_initialized = False


def init_encoders():
    """
    Initialize left and right wheel encoders.

    Returns:
        True if initialization succeeds, otherwise False.
    """
    global _left_encoder
    global _right_encoder
    global _encoders_initialized

    try:
        _left_encoder = RotaryEncoder(
            a=config.ENCODER_LEFT_A,
            b=config.ENCODER_LEFT_B,
            max_steps=0
        )

        _right_encoder = RotaryEncoder(
            a=config.ENCODER_RIGHT_A,
            b=config.ENCODER_RIGHT_B,
            max_steps=0
        )

        _encoders_initialized = True

        print("Wheel encoders initialized.")
        return True

    except Exception as error:
        _left_encoder = None
        _right_encoder = None
        _encoders_initialized = False

        print(f"Encoder initialization failed: {error}")
        return False


def _check_initialized():
    """
    Check whether encoders are initialized.
    """
    if not _encoders_initialized:
        raise RuntimeError(
            "Encoders are not initialized. "
            "Call init_encoders() first."
        )


def get_encoder_counts():
    """
    Get current encoder step counts.

    Returns:
        Tuple containing:
        (left_count, right_count)
    """
    _check_initialized()

    left_count = _left_encoder.steps
    right_count = _right_encoder.steps

    return left_count, right_count


def get_left_encoder_count():
    """
    Get the left encoder count.
    """
    _check_initialized()
    return _left_encoder.steps


def get_right_encoder_count():
    """
    Get the right encoder count.
    """
    _check_initialized()
    return _right_encoder.steps


def reset_encoder_counts():
    """
    Reset both encoder counts to zero.
    """
    _check_initialized()

    _left_encoder.steps = 0
    _right_encoder.steps = 0

    print("Encoder counts reset.")


def get_left_distance_mm():
    """
    Calculate left wheel distance in millimeters.
    """
    _check_initialized()

    wheel_circumference_mm = (
        config.WHEEL_DIAMETER_MM * 3.141592653589793
    )

    left_count = _left_encoder.steps

    distance_mm = (
        left_count
        * wheel_circumference_mm
        / config.ENCODER_PPR
    )

    return distance_mm


def get_right_distance_mm():
    """
    Calculate right wheel distance in millimeters.
    """
    _check_initialized()

    wheel_circumference_mm = (
        config.WHEEL_DIAMETER_MM * 3.141592653589793
    )

    right_count = _right_encoder.steps

    distance_mm = (
        right_count
        * wheel_circumference_mm
        / config.ENCODER_PPR
    )

    return distance_mm


def get_average_distance_mm():
    """
    Calculate average distance travelled by both wheels.
    """
    left_distance = get_left_distance_mm()
    right_distance = get_right_distance_mm()

    return (left_distance + right_distance) / 2.0


def get_average_distance_cm():
    """
    Return average wheel distance in centimeters.
    """
    return get_average_distance_mm() / 10.0


def get_average_distance_m():
    """
    Return average wheel distance in meters.
    """
    return get_average_distance_mm() / 1000.0


def cleanup_encoders():
    """
    Release encoder GPIO resources.
    """
    global _left_encoder
    global _right_encoder
    global _encoders_initialized

    try:
        if _left_encoder is not None:
            _left_encoder.close()

        if _right_encoder is not None:
            _right_encoder.close()

    except Exception as error:
        print(f"Encoder cleanup warning: {error}")

    _left_encoder = None
    _right_encoder = None
    _encoders_initialized = False

    print("Encoder resources released.")


def test_encoders():
    """
    Display encoder counts and distance continuously.
    Press Ctrl+C to stop.
    """
    import time

    if not init_encoders():
        print("Cannot test encoders.")
        return

    reset_encoder_counts()

    print("Encoder test started.")
    print("Move the robot wheels by hand.")
    print("Press Ctrl+C to stop.")

    try:
        while True:
            left_count, right_count = get_encoder_counts()
            distance_cm = get_average_distance_cm()

            print(
                f"Left: {left_count} | "
                f"Right: {right_count} | "
                f"Distance: {distance_cm:.2f} cm"
            )

            time.sleep(0.25)

    except KeyboardInterrupt:
        print("\nEncoder test stopped.")

    finally:
        cleanup_encoders()


if __name__ == "__main__":
    test_encoders()


"""
INDOOR DELIVERY ROBOT
File: delivery.py

Delivery destination management and basic room navigation.
"""

import time

import config
import navigation


_delivery_active = False
_current_location = "HOME"


def get_current_location():
    """
    Return the robot's estimated current location.
    """
    return _current_location


def is_delivery_active():
    """
    Check whether a delivery is currently active.
    """
    return _delivery_active


def get_destinations():
    """
    Return available delivery destinations.
    """
    return list(config.DELIVERY_LOCATIONS.keys())


def _set_location(location):
    """
    Update the estimated location.
    """
    global _current_location
    _current_location = location


def _validate_destination(destination):
    """
    Check whether the destination exists.
    """
    return destination in config.DELIVERY_LOCATIONS


def _move_to_destination(destination):
    """
    Basic route execution using configured room coordinates.

    This initial version supports simple axis-aligned routes:
    move along X, then rotate and move along Y.

    Coordinates are in millimeters.
    """
    global _current_location

    target_x, target_y = config.DELIVERY_LOCATIONS[destination]

    current_x, current_y = config.DELIVERY_LOCATIONS.get(
        _current_location,
        (0, 0)
    )

    delta_x = target_x - current_x
    delta_y = target_y - current_y

    # Move along X axis.
    if delta_x != 0:
        if delta_x < 0:
            navigation.turn_left_90()
        else:
            navigation.turn_right_90()

        if not navigation.move_distance_cm(abs(delta_x) / 10):
            return False

    # Move along Y axis.
    if delta_y != 0:
        if delta_y < 0:
            navigation.turn_left_90()
        else:
            navigation.turn_right_90()

        if not navigation.move_distance_cm(abs(delta_y) / 10):
            return False

    _set_location(destination)

    return True


def start_delivery(destination):
    """
    Start a delivery to the requested destination.

    Returns True if the route completes.
    """
    global _delivery_active

    if _delivery_active:
        print("A delivery is already in progress.")
        return False

    if not _validate_destination(destination):
        print(f"Unknown destination: {destination}")
        print("Available destinations:", get_destinations())
        return False

    _delivery_active = True

    start_time = time.monotonic()

    try:
        print(f"Delivery started: {destination}")

        if not navigation.init_navigation():
            print("Navigation initialization failed.")
            return False

        success = _move_to_destination(destination)

        if success:
            print(f"Arrived at {destination}.")
        else:
            print("Delivery stopped before reaching destination.")

        elapsed = time.monotonic() - start_time

        if elapsed > config.MAX_DELIVERY_TIME_SECONDS:
            print("Delivery exceeded maximum allowed time.")

        return success

    except Exception as error:
        navigation.stop()
        print(f"Delivery error: {error}")
        return False

    finally:
        navigation.stop()
        navigation.cleanup_navigation()
        _delivery_active = False


def return_home():
    """
    Return the robot to HOME using the same basic route method.
    """
    global _delivery_active

    if _delivery_active:
        print("Cannot return home: delivery already active.")
        return False

    if _current_location == "HOME":
        print("Robot is already at HOME.")
        return True

    _delivery_active = True

    try:
        if not navigation.init_navigation():
            print("Navigation initialization failed.")
            return False

        success = _move_to_destination("HOME")

        if success:
            print("Robot returned HOME.")
        else:
            print("Return-home route failed.")

        return success

    except Exception as error:
        navigation.stop()
        print(f"Return-home error: {error}")
        return False

    finally:
        navigation.stop()
        navigation.cleanup_navigation()
        _delivery_active = False


def cancel_delivery():
    """
    Stop the robot immediately.
    """
    navigation.stop()
    print("Delivery cancelled.")


def test_delivery():
    """
    Test a delivery to the configured default destination.
    """
    destination = config.DEFAULT_DESTINATION

    print(f"Testing delivery to {destination}...")
    start_delivery(destination)


if __name__ == "__main__":
    test_delivery()

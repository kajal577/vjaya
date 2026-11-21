
"""
INDOOR DELIVERY ROBOT
File: sensors.py

VL53L0X distance sensor functions.
"""

import board
import adafruit_vl53l0x

import config


_sensor = None
_i2c = None
_sensor_initialized = False


def init_sensors():
    """
    Initialize the VL53L0X distance sensor.
    Returns True if initialization succeeds, otherwise False.
    """
    global _sensor, _i2c, _sensor_initialized

    try:
        _i2c = board.I2C()
        _sensor = adafruit_vl53l0x.VL53L0X(_i2c)

        _sensor_initialized = True

        print("VL53L0X distance sensor initialized.")
        return True

    except Exception as error:
        _sensor = None
        _sensor_initialized = False

        print(f"Sensor initialization failed: {error}")
        return False


def read_distance_cm():
    """
    Read distance from the VL53L0X sensor.

    Returns:
        Distance in centimeters as a float.
        None if the sensor is unavailable or reading fails.
    """
    if not _sensor_initialized or _sensor is None:
        return None

    try:
        distance_mm = _sensor.range
        distance_cm = distance_mm / 10.0

        if distance_cm <= 0:
            return None

        return round(distance_cm, 1)

    except Exception as error:
        print(f"Distance reading error: {error}")
        return None


def obstacle_detected():
    """
    Returns True if an obstacle is within the configured
    obstacle distance.

    Sensor failure is treated as an obstacle for safety.
    """
    distance_cm = read_distance_cm()

    if distance_cm is None:
        return True

    return distance_cm <= config.OBSTACLE_DISTANCE_CM


def emergency_obstacle_detected():
    """
    Returns True if an obstacle is within the emergency
    stopping distance.

    Sensor failure is treated as an emergency stop.
    """
    distance_cm = read_distance_cm()

    if distance_cm is None:
        return True

    return distance_cm <= config.EMERGENCY_STOP_DISTANCE_CM


def cleanup_sensors():
    """
    Release the I2C sensor resources.
    """
    global _sensor, _i2c, _sensor_initialized

    try:
        if _i2c is not None:
            _i2c.deinit()

    except Exception as error:
        print(f"Sensor cleanup warning: {error}")

    _sensor = None
    _i2c = None
    _sensor_initialized = False

    print("Distance sensor resources released.")


def test_sensor():
    """
    Continuously display distance readings.
    Press Ctrl+C to stop the test.
    """
    import time

    if not init_sensors():
        print("Cannot test sensor: initialization failed.")
        return

    print("Distance sensor test started.")
    print("Press Ctrl+C to stop.")

    try:
        while True:
            distance_cm = read_distance_cm()

            if distance_cm is None:
                print("Distance: SENSOR ERROR")
            else:
                print(f"Distance: {distance_cm} cm")

            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nSensor test stopped.")

    finally:
        cleanup_sensors()


if __name__ == "__main__":
    test_sensor()

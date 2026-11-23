
"""
============================================================
VJaYa Robotics
PROJECT 07: SMART PARKING SYSTEM
File: sensors.py

IR Sensor and Parking Slot Monitoring
Hardware: Raspberry Pi 5
============================================================
"""

import logging
import time

from gpiozero import DigitalInputDevice

from config import (
    ENTRY_SENSOR_PIN,
    EXIT_SENSOR_PIN,
    PARKING_SENSOR_PINS,
    SENSOR_POLL_INTERVAL,
)

logger = logging.getLogger(__name__)


class ParkingSensors:

    def __init__(self, active_low=True):

        self.active_low = active_low

        self.entry_sensor = None
        self.exit_sensor = None

        self.slot_sensors = {}

        self.initialized = False

        self.last_readings = {}

    # --------------------------------------------------------
    # CREATE SENSOR
    # --------------------------------------------------------

    def create_sensor(self, pin):

        try:

            sensor = DigitalInputDevice(
                pin=pin,
                pull_up=self.active_low,
                active_state=not self.active_low
            )

            logger.info(
                "Sensor initialized on GPIO %s",
                pin
            )

            return sensor

        except Exception as error:

            logger.exception(
                "Failed to initialize GPIO %s: %s",
                pin,
                error
            )

            return None

    # --------------------------------------------------------
    # INITIALIZE ALL SENSORS
    # --------------------------------------------------------

    def initialize(self):

        logger.info("Initializing parking sensors...")

        self.entry_sensor = self.create_sensor(
            ENTRY_SENSOR_PIN
        )

        self.exit_sensor = self.create_sensor(
            EXIT_SENSOR_PIN
        )

        for slot_id, pin in PARKING_SENSOR_PINS.items():

            sensor = self.create_sensor(pin)

            self.slot_sensors[slot_id] = sensor

        self.initialized = (
            self.entry_sensor is not None
            and self.exit_sensor is not None
            and all(
                sensor is not None
                for sensor in self.slot_sensors.values()
            )
        )

        if self.initialized:

            logger.info(
                "All parking sensors initialized."
            )

        else:

            logger.error(
                "One or more parking sensors failed."
            )

        return self.initialized

    # --------------------------------------------------------
    # READ INDIVIDUAL SENSOR
    # --------------------------------------------------------

    def read_sensor(self, sensor):

        if sensor is None:
            return None

        try:

            return sensor.is_active

        except Exception as error:

            logger.error(
                "Sensor reading failed: %s",
                error
            )

            return None

    # --------------------------------------------------------
    # CHECK ENTRANCE VEHICLE
    # --------------------------------------------------------

    def is_vehicle_at_entry(self):

        return self.read_sensor(
            self.entry_sensor
        )

    # --------------------------------------------------------
    # CHECK EXIT VEHICLE
    # --------------------------------------------------------

    def is_vehicle_at_exit(self):

        return self.read_sensor(
            self.exit_sensor
        )

    # --------------------------------------------------------
    # CHECK PARKING SLOT
    # --------------------------------------------------------

    def is_slot_occupied(self, slot_id):

        sensor = self.slot_sensors.get(slot_id)

        return self.read_sensor(sensor)

    # --------------------------------------------------------
    # GET ALL PARKING SLOT STATES
    # --------------------------------------------------------

    def get_all_slot_states(self):

        states = {}

        for slot_id in PARKING_SENSOR_PINS:

            states[slot_id] = self.is_slot_occupied(
                slot_id
            )

        self.last_readings = states.copy()

        return states

    # --------------------------------------------------------
    # GET AVAILABLE PARKING SLOTS
    # --------------------------------------------------------

    def get_available_slots(self):

        states = self.get_all_slot_states()

        available = []

        for slot_id, occupied in states.items():

            # Unknown sensor readings are not considered free
            if occupied is False:

                available.append(slot_id)

        return available

    # --------------------------------------------------------
    # GET OCCUPIED PARKING SLOTS
    # --------------------------------------------------------

    def get_occupied_slots(self):

        states = self.get_all_slot_states()

        occupied = []

        for slot_id, state in states.items():

            if state is True:

                occupied.append(slot_id)

        return occupied

    # --------------------------------------------------------
    # GET SENSOR STATUS
    # --------------------------------------------------------

    def get_sensor_status(self):

        return {
            "initialized": self.initialized,

            "entry_sensor": self.is_vehicle_at_entry(),

            "exit_sensor": self.is_vehicle_at_exit(),

            "parking_slots": self.get_all_slot_states()
        }

    # --------------------------------------------------------
    # WAIT FOR VEHICLE AT ENTRANCE
    # --------------------------------------------------------

    def wait_for_entry_vehicle(
        self,
        timeout=30
    ):

        start_time = time.monotonic()

        while time.monotonic() - start_time < timeout:

            detected = self.is_vehicle_at_entry()

            if detected is True:

                logger.info(
                    "Vehicle detected at entrance."
                )

                return True

            if detected is None:

                logger.error(
                    "Entrance sensor unavailable."
                )

                return False

            time.sleep(SENSOR_POLL_INTERVAL)

        logger.info(
            "Entrance detection timed out."
        )

        return False

    # --------------------------------------------------------
    # WAIT FOR VEHICLE AT EXIT
    # --------------------------------------------------------

    def wait_for_exit_vehicle(
        self,
        timeout=30
    ):

        start_time = time.monotonic()

        while time.monotonic() - start_time < timeout:

            detected = self.is_vehicle_at_exit()

            if detected is True:

                logger.info(
                    "Vehicle detected at exit."
                )

                return True

            if detected is None:

                logger.error(
                    "Exit sensor unavailable."
                )

                return False

            time.sleep(SENSOR_POLL_INTERVAL)

        logger.info(
            "Exit detection timed out."
        )

        return False

    # --------------------------------------------------------
    # CLOSE ALL SENSORS
    # --------------------------------------------------------

    def close(self):

        sensors = [
            self.entry_sensor,
            self.exit_sensor
        ]

        sensors.extend(
            self.slot_sensors.values()
        )

        for sensor in sensors:

            if sensor is not None:

                try:
                    sensor.close()

                except Exception as error:

                    logger.warning(
                        "Sensor shutdown error: %s",
                        error
                    )

        self.entry_sensor = None
        self.exit_sensor = None

        self.slot_sensors.clear()

        self.initialized = False

        logger.info(
            "All parking sensors closed."
        )

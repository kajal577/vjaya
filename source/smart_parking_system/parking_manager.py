
"""
============================================================
VJaYa Robotics
PROJECT 07: SMART PARKING SYSTEM
File: parking_manager.py

Parking Slot Allocation and Management
============================================================
"""

import logging
import threading

from config import (
    TOTAL_PARKING_SLOTS,
    PARKING_SLOT_NAMES
)

from database import ParkingDatabase
from sensors import ParkingSensors

logger = logging.getLogger(__name__)


class ParkingManager:

    def __init__(
        self,
        database=None,
        sensors=None
    ):

        self.database = database or ParkingDatabase()
        self.sensors = sensors

        self.lock = threading.RLock()

        self.total_slots = TOTAL_PARKING_SLOTS

        self.slot_names = PARKING_SLOT_NAMES.copy()

    # --------------------------------------------------------
    # INITIALIZE PARKING SYSTEM
    # --------------------------------------------------------

    def initialize(self):

        try:

            success = self.database.initialize_slots(
                self.slot_names
            )

            if not success:
                logger.error(
                    "Parking slot initialization failed."
                )
                return False

            logger.info(
                "Parking manager initialized with %s slots.",
                self.total_slots
            )

            return True

        except Exception as error:

            logger.exception(
                "Parking manager initialization error: %s",
                error
            )

            return False

    # --------------------------------------------------------
    # GET SENSOR SLOT STATES
    # --------------------------------------------------------

    def get_sensor_states(self):

        if self.sensors is None:
            return None

        if not self.sensors.initialized:
            return None

        states = self.sensors.get_all_slot_states()

        if any(value is None for value in states.values()):
            return None

        return states

    # --------------------------------------------------------
    # GET AVAILABLE SLOTS
    # --------------------------------------------------------

    def get_available_slots(self):

        with self.lock:

            sensor_states = self.get_sensor_states()

            if sensor_states is None:
                logger.error(
                    "Cannot determine slot availability."
                )
                return []

            database_states = {
                row[0]: bool(row[1])
                for row in self.database.get_slot_status()
            }

            available = []

            for index, slot_name in enumerate(
                self.slot_names, start=1
            ):

                sensor_occupied = sensor_states.get(index)

                database_occupied = database_states.get(
                    slot_name, False
                )

                if (
                    sensor_occupied is False
                    and database_occupied is False
                ):

                    available.append(slot_name)

            return available

    # --------------------------------------------------------
    # GET OCCUPIED SLOTS
    # --------------------------------------------------------

    def get_occupied_slots(self):

        with self.lock:

            sensor_states = self.get_sensor_states()

            if sensor_states is None:
                return []

            occupied = []

            for index, slot_name in enumerate(
                self.slot_names, start=1
            ):

                if sensor_states.get(index) is True:

                    occupied.append(slot_name)

            return occupied

    # --------------------------------------------------------
    # ALLOCATE PARKING SLOT
    # --------------------------------------------------------

    def allocate_slot(
        self,
        plate_number,
        entry_image=None
    ):

        with self.lock:

            try:

                # Prevent duplicate active vehicle
                if self.database.is_vehicle_parked(
                    plate_number
                ):

                    logger.warning(
                        "Vehicle already parked: %s",
                        plate_number
                    )

                    return None

                available_slots = self.get_available_slots()

                if not available_slots:

                    logger.warning(
                        "No parking slots available."
                    )

                    return None

                selected_slot = available_slots[0]

                vehicle_id = self.database.register_entry(
                    plate_number=plate_number,
                    parking_slot=selected_slot,
                    entry_image=entry_image
                )

                if vehicle_id is None:
                    return None

                logger.info(
                    "Vehicle %s allocated to %s",
                    plate_number,
                    selected_slot
                )

                return {
                    "vehicle_id": vehicle_id,
                    "plate_number": plate_number,
                    "parking_slot": selected_slot
                }

            except Exception as error:

                logger.exception(
                    "Slot allocation failed: %s",
                    error
                )

                return None

    # --------------------------------------------------------
    # RELEASE PARKING SLOT
    # --------------------------------------------------------

    def release_slot(
        self,
        plate_number,
        parking_fee=0,
        exit_image=None
    ):

        with self.lock:

            try:

                vehicle = self.database.get_vehicle(
                    plate_number
                )

                if vehicle is None:
                    logger.warning(
                        "Vehicle record not found."
                    )
                    return False

                # Database columns:
                # id, plate_number, entry_time, exit_time,
                # parking_slot, status, entry_image,
                # exit_image, parking_fee

                if vehicle[5] != "PARKED":

                    logger.warning(
                        "Vehicle is not currently parked."
                    )

                    return False

                success = self.database.register_exit(
                    plate_number=plate_number,
                    parking_fee=parking_fee,
                    exit_image=exit_image
                )

                if success:

                    logger.info(
                        "Parking slot released for %s",
                        plate_number
                    )

                return success

            except Exception as error:

                logger.exception(
                    "Slot release failed: %s",
                    error
                )

                return False

    # --------------------------------------------------------
    # GET PARKING STATISTICS
    # --------------------------------------------------------

    def get_statistics(self):

        with self.lock:

            sensor_states = self.get_sensor_states()

            if sensor_states is None:

                return {
                    "total_slots": self.total_slots,
                    "available_slots": None,
                    "occupied_slots": None,
                    "unknown_slots": self.total_slots,
                    "system_status": "SENSOR_ERROR"
                }

            available = 0
            occupied = 0
            unknown = 0

            for index in range(1, self.total_slots + 1):

                state = sensor_states.get(index)

                if state is True:
                    occupied += 1

                elif state is False:
                    available += 1

                else:
                    unknown += 1

            return {
                "total_slots": self.total_slots,
                "available_slots": available,
                "occupied_slots": occupied,
                "unknown_slots": unknown,
                "system_status": "ONLINE"
            }

    # --------------------------------------------------------
    # CHECK PARKING AVAILABILITY
    # --------------------------------------------------------

    def has_available_space(self):

        return len(
            self.get_available_slots()
        ) > 0

    # --------------------------------------------------------
    # GET PARKED VEHICLES
    # --------------------------------------------------------

    def get_current_vehicles(self):

        return self.database.get_parked_vehicles()

    # --------------------------------------------------------
    # GET SLOT DETAILS
    # --------------------------------------------------------

    def get_slot_details(self):

        sensor_states = self.get_sensor_states()

        if sensor_states is None:
            return None

        database_states = {
            row[0]: {
                "occupied": bool(row[1]),
                "vehicle_id": row[2]
            }
            for row in self.database.get_slot_status()
        }

        details = []

        for index, slot_name in enumerate(
            self.slot_names, start=1
        ):

            sensor_occupied = sensor_states.get(index)

            database_info = database_states.get(
                slot_name,
                {}
            )

            details.append({
                "slot": slot_name,
                "sensor_occupied": sensor_occupied,
                "database_occupied": database_info.get(
                    "occupied"
                ),
                "vehicle_id": database_info.get(
                    "vehicle_id"
                ),
                "status": (
                    "UNKNOWN"
                    if sensor_occupied is None
                    else "OCCUPIED"
                    if sensor_occupied
                    else "AVAILABLE"
                )
            })

        return details

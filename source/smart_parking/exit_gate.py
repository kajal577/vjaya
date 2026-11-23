
"""
============================================================
VJaYa Robotics
PROJECT 07: SMART PARKING SYSTEM
File: exit_gate.py

Automatic Parking Exit Barrier Controller
Hardware: SG90 Servo Motor
GPIO: 19 (BCM)
============================================================
"""

import logging
import time
import threading

from gpiozero import AngularServo

from config import (
    EXIT_SERVO_PIN,
    GATE_CLOSED_ANGLE,
    GATE_OPEN_ANGLE,
    GATE_OPEN_DURATION
)

logger = logging.getLogger(__name__)


class ExitGate:

    def __init__(self):

        self.servo = None

        self.is_open = False
        self.is_initialized = False

        self.lock = threading.RLock()

    # --------------------------------------------------------
    # INITIALIZE EXIT SERVO
    # --------------------------------------------------------

    def initialize(self):

        try:

            logger.info(
                "Initializing exit gate servo..."
            )

            self.servo = AngularServo(
                EXIT_SERVO_PIN,
                min_angle=0,
                max_angle=180,
                min_pulse_width=0.0005,
                max_pulse_width=0.0025
            )

            self.servo.angle = GATE_CLOSED_ANGLE

            time.sleep(0.5)

            self.is_open = False
            self.is_initialized = True

            logger.info(
                "Exit gate initialized successfully."
            )

            return True

        except Exception as error:

            logger.exception(
                "Exit gate initialization failed: %s",
                error
            )

            self.servo = None
            self.is_initialized = False

            return False

    # --------------------------------------------------------
    # OPEN EXIT GATE
    # --------------------------------------------------------

    def open_gate(self, authorized=False):

        with self.lock:

            if not self.is_initialized:

                logger.error(
                    "Exit gate is not initialized."
                )

                return False

            if not authorized:

                logger.warning(
                    "Unauthorized exit gate operation."
                )

                return False

            try:

                logger.info(
                    "Opening parking exit barrier..."
                )

                self.servo.angle = GATE_OPEN_ANGLE

                time.sleep(0.7)

                self.is_open = True

                logger.info(
                    "Exit barrier opened."
                )

                return True

            except Exception as error:

                logger.exception(
                    "Exit barrier opening failed: %s",
                    error
                )

                return False

    # --------------------------------------------------------
    # CLOSE EXIT GATE
    # --------------------------------------------------------

    def close_gate(self):

        with self.lock:

            if not self.is_initialized:

                logger.error(
                    "Exit gate is not initialized."
                )

                return False

            try:

                logger.info(
                    "Closing parking exit barrier..."
                )

                self.servo.angle = GATE_CLOSED_ANGLE

                time.sleep(0.7)

                self.is_open = False

                logger.info(
                    "Exit barrier closed."
                )

                return True

            except Exception as error:

                logger.exception(
                    "Exit barrier closing failed: %s",
                    error
                )

                return False

    # --------------------------------------------------------
    # AUTOMATIC EXIT GATE CONTROL
    # --------------------------------------------------------

    def open_for_vehicle(
        self,
        authorized=False,
        duration=GATE_OPEN_DURATION
    ):

        if not authorized:

            logger.warning(
                "Vehicle exit authorization failed."
            )

            return False

        if not self.open_gate(authorized=True):
            return False

        try:

            logger.info(
                "Waiting for vehicle to pass through exit..."
            )

            time.sleep(max(0, duration))

            return self.close_gate()

        except Exception as error:

            logger.exception(
                "Automatic exit gate operation failed: %s",
                error
            )

            return False

    # --------------------------------------------------------
    # EXIT GATE STATUS
    # --------------------------------------------------------

    def get_status(self):

        return {
            "initialized": self.is_initialized,
            "is_open": self.is_open,
            "state": (
                "OPEN"
                if self.is_open
                else "CLOSED"
            )
        }

    # --------------------------------------------------------
    # SHUTDOWN
    # --------------------------------------------------------

    def shutdown(self):

        with self.lock:

            if self.servo is None:
                return

            try:

                if self.is_open:
                    self.close_gate()

                self.servo.detach()
                self.servo.close()

                logger.info(
                    "Exit gate controller stopped."
                )

            except Exception as error:

                logger.exception(
                    "Exit gate shutdown failed: %s",
                    error
                )

            finally:

                self.servo = None
                self.is_initialized = False
                self.is_open = False

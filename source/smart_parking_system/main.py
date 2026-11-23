
"""
============================================================
VJaYa Robotics
PROJECT 07: SMART PARKING SYSTEM
File: main.py

Main Application Controller
Hardware: Raspberry Pi 5
Camera: Raspberry Pi Camera Module 3
============================================================
"""

import logging
import signal
import sys
import threading
import time

from config import TOTAL_PARKING_SLOTS

from camera import ParkingCamera
from vehicle_detection import VehicleDetector
from plate_recognition import PlateRecognizer
from image_processing import ImageProcessor

from database import ParkingDatabase
from sensors import ParkingSensors
from parking_manager import ParkingManager

from entry_gate import EntryGate
from exit_gate import ExitGate

from lcd_display import LCDDisplay
from fee_calculator import ParkingFeeCalculator

from dashboard import start_dashboard

from logging_config import setup_logging


# ------------------------------------------------------------
# LOGGING
# ------------------------------------------------------------

setup_logging()

logger = logging.getLogger("SmartParkingMain")


# ------------------------------------------------------------
# SMART PARKING APPLICATION
# ------------------------------------------------------------

class SmartParkingSystem:

    def __init__(self):

        self.running = False

        self.camera = None
        self.vehicle_detector = None
        self.plate_recognizer = None
        self.image_processor = None

        self.database = None
        self.sensors = None
        self.parking_manager = None

        self.entry_gate = None
        self.exit_gate = None

        self.lcd = None
        self.fee_calculator = None

        self.dashboard_thread = None

        self.initialized = False

    # --------------------------------------------------------
    # INITIALIZE ALL MODULES
    # --------------------------------------------------------

    def initialize(self):

        logger.info("Starting Smart Parking System...")

        try:

            # DATABASE

            logger.info("Initializing database...")

            self.database = ParkingDatabase()

            # SENSORS

            logger.info("Initializing parking sensors...")

            self.sensors = ParkingSensors()

            if not self.sensors.initialized:
                raise RuntimeError(
                    "Parking sensors initialization failed."
                )

            # PARKING MANAGER

            logger.info("Initializing parking manager...")

            self.parking_manager = ParkingManager(
                database=self.database,
                sensors=self.sensors
            )

            # ENTRY GATE

            logger.info("Initializing entry gate...")

            self.entry_gate = EntryGate()

            if not self.entry_gate.initialize():
                raise RuntimeError(
                    "Entry gate initialization failed."
                )

            # EXIT GATE

            logger.info("Initializing exit gate...")

            self.exit_gate = ExitGate()

            if not self.exit_gate.initialize():
                raise RuntimeError(
                    "Exit gate initialization failed."
                )

            # LCD DISPLAY

            logger.info("Initializing LCD display...")

            self.lcd = LCDDisplay()

            if not self.lcd.initialize():
                logger.warning(
                    "LCD unavailable. Continuing without display."
                )
                self.lcd = None

            # CAMERA

            logger.info("Preparing camera module...")

            self.camera = ParkingCamera()

            # IMAGE PROCESSING

            self.image_processor = ImageProcessor()

            # NUMBER PLATE RECOGNITION

            self.plate_recognizer = PlateRecognizer()

            # VEHICLE DETECTION

            self.vehicle_detector = VehicleDetector(
                self.camera
            )

            # PARKING FEE CALCULATOR

            self.fee_calculator = ParkingFeeCalculator()

            self.initialized = True

            if self.lcd:
                self.lcd.show_welcome()

            logger.info(
                "Smart Parking System initialized successfully."
            )

            return True

        except Exception:

            logger.exception(
                "Smart Parking initialization failed."
            )

            self.shutdown()

            return False

    # --------------------------------------------------------
    # START WEB DASHBOARD
    # --------------------------------------------------------

    def start_web_dashboard(self):

        try:

            self.dashboard_thread = threading.Thread(
                target=start_dashboard,
                kwargs={
                    "host": "0.0.0.0",
                    "port": 5000,
                    "debug": False
                },
                daemon=True
            )

            self.dashboard_thread.start()

            logger.info(
                "Parking dashboard started on port 5000."
            )

        except Exception:

            logger.exception(
                "Dashboard startup failed."
            )

    # --------------------------------------------------------
    # DISPLAY PARKING STATUS
    # --------------------------------------------------------

    def update_parking_status(self):

        try:

            status = self.parking_manager.get_slot_details()

            logger.info(
                "Parking status: %s",
                status
            )

        except Exception:

            logger.exception(
                "Unable to update parking status."
            )

    # --------------------------------------------------------
    # MAIN APPLICATION LOOP
    # --------------------------------------------------------

    def run(self):

        if not self.initialized:

            logger.error(
                "System is not initialized."
            )

            return

        self.running = True

        logger.info(
            "Smart Parking System is running."
        )

        self.start_web_dashboard()

        try:

            while self.running:

                self.update_parking_status()

                time.sleep(5)

        except KeyboardInterrupt:

            logger.info(
                "Keyboard interruption received."
            )

        except Exception:

            logger.exception(
                "Main application error."
            )

        finally:

            self.shutdown()

    # --------------------------------------------------------
    # STOP APPLICATION
    # --------------------------------------------------------

    def stop(self):

        logger.info(
            "Stopping Smart Parking System..."
        )

        self.running = False

    # --------------------------------------------------------
    # SAFE SHUTDOWN
    # --------------------------------------------------------

    def shutdown(self):

        logger.info(
            "Shutting down Smart Parking System..."
        )

        self.running = False

        # Close entry gate

        if self.entry_gate:

            try:
                self.entry_gate.shutdown()
            except Exception:
                logger.exception("Entry gate shutdown error.")

        # Close exit gate

        if self.exit_gate:

            try:
                self.exit_gate.shutdown()
            except Exception:
                logger.exception("Exit gate shutdown error.")

        # Stop camera

        if self.camera:

            try:
                self.camera.stop()
            except Exception:
                logger.exception("Camera shutdown error.")

        # Stop LCD

        if self.lcd:

            try:
                self.lcd.shutdown()
            except Exception:
                logger.exception("LCD shutdown error.")

        # Release sensors

        if self.sensors:

            try:
                self.sensors.close()
            except Exception:
                logger.exception("Sensor shutdown error.")

        self.initialized = False

        logger.info(
            "Smart Parking System stopped."
        )


# ------------------------------------------------------------
# APPLICATION ENTRY POINT
# ------------------------------------------------------------

def main():

    parking_system = SmartParkingSystem()

    def handle_shutdown(signum, frame):

        logger.info(
            "Shutdown signal received: %s",
            signum
        )

        parking_system.stop()

    signal.signal(
        signal.SIGINT,
        handle_shutdown
    )

    signal.signal(
        signal.SIGTERM,
        handle_shutdown
    )

    if parking_system.initialize():

        parking_system.run()

    else:

        logger.error(
            "Unable to start Smart Parking System."
        )

        sys.exit(1)


if __name__ == "__main__":

    main()

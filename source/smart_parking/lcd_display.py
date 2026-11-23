
"""
============================================================
VJaYa Robotics
PROJECT 07: SMART PARKING SYSTEM
File: lcd_display.py

16x2 I2C LCD Display Controller
============================================================
"""

import logging
import time
import threading

from RPLCD.i2c import CharLCD

from config import (
    LCD_I2C_ADDRESS,
    LCD_COLUMNS,
    LCD_ROWS
)

logger = logging.getLogger(__name__)


class LCDDisplay:

    def __init__(self):

        self.lcd = None
        self.is_initialized = False

        self.lock = threading.RLock()

    # --------------------------------------------------------
    # INITIALIZE LCD
    # --------------------------------------------------------

    def initialize(self):

        try:

            logger.info("Initializing LCD display...")

            self.lcd = CharLCD(
                i2c_expander="PCF8574",
                address=LCD_I2C_ADDRESS,
                port=1,
                cols=LCD_COLUMNS,
                rows=LCD_ROWS,
                charmap="A02",
                auto_linebreaks=False
            )

            self.lcd.clear()

            self.is_initialized = True

            self.show_message(
                "VJaYa Robotics",
                "Smart Parking"
            )

            time.sleep(2)

            logger.info("LCD initialized successfully.")

            return True

        except Exception as error:

            logger.exception(
                "LCD initialization failed: %s",
                error
            )

            self.lcd = None
            self.is_initialized = False

            return False

    # --------------------------------------------------------
    # CLEAR LCD
    # --------------------------------------------------------

    def clear(self):

        if not self.is_initialized:
            return False

        with self.lock:

            try:

                self.lcd.clear()

                return True

            except Exception as error:

                logger.error(
                    "LCD clear failed: %s",
                    error
                )

                return False

    # --------------------------------------------------------
    # DISPLAY TWO LINES
    # --------------------------------------------------------

    def show_message(
        self,
        line1="",
        line2=""
    ):

        if not self.is_initialized:
            return False

        with self.lock:

            try:

                self.lcd.clear()

                self.lcd.cursor_pos = (0, 0)
                self.lcd.write_string(
                    str(line1)[:LCD_COLUMNS].ljust(LCD_COLUMNS)
                )

                self.lcd.cursor_pos = (1, 0)
                self.lcd.write_string(
                    str(line2)[:LCD_COLUMNS].ljust(LCD_COLUMNS)
                )

                return True

            except Exception as error:

                logger.error(
                    "LCD message error: %s",
                    error
                )

                return False

    # --------------------------------------------------------
    # WELCOME SCREEN
    # --------------------------------------------------------

    def show_welcome(self):

        return self.show_message(
            "SMART PARKING",
            "Welcome!"
        )

    # --------------------------------------------------------
    # PARKING AVAILABILITY
    # --------------------------------------------------------

    def show_available_slots(self, available, total):

        return self.show_message(
            "Parking Slots:",
            f"{available}/{total} Available"
        )

    # --------------------------------------------------------
    # PARKING FULL
    # --------------------------------------------------------

    def show_parking_full(self):

        return self.show_message(
            "PARKING FULL!",
            "Please Wait"
        )

    # --------------------------------------------------------
    # RECOGNIZED NUMBER PLATE
    # --------------------------------------------------------

    def show_number_plate(self, plate_number):

        plate = str(plate_number).upper()

        return self.show_message(
            "Vehicle Number:",
            plate
        )

    # --------------------------------------------------------
    # VEHICLE ENTRY
    # --------------------------------------------------------

    def show_entry_success(self, slot):

        return self.show_message(
            "Entry Approved",
            f"Slot: {slot}"
        )

    # --------------------------------------------------------
    # VEHICLE EXIT
    # --------------------------------------------------------

    def show_exit_success(self, fee):

        return self.show_message(
            "Exit Approved",
            f"Fee: Rs.{fee}"
        )

    # --------------------------------------------------------
    # UNKNOWN VEHICLE
    # --------------------------------------------------------

    def show_access_denied(self):

        return self.show_message(
            "ACCESS DENIED",
            "Check Number"
        )

    # --------------------------------------------------------
    # PROCESSING MESSAGE
    # --------------------------------------------------------

    def show_processing(self):

        return self.show_message(
            "Please Wait...",
            "Scanning Plate"
        )

    # --------------------------------------------------------
    # SHUTDOWN
    # --------------------------------------------------------

    def shutdown(self):

        with self.lock:

            if self.lcd is None:
                return

            try:

                self.lcd.clear()
                self.lcd.close()

                logger.info(
                    "LCD display stopped."
                )

            except Exception as error:

                logger.error(
                    "LCD shutdown failed: %s",
                    error
                )

            finally:

                self.lcd = None
                self.is_initialized = False

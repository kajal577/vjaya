
"""
============================================================
VJaYa Robotics
PROJECT 07: SMART PARKING SYSTEM
File: fee_calculator.py

Parking Duration and Fee Calculator
============================================================
"""

import logging
import math

from datetime import datetime

from config import (
    PARKING_FEE_PER_HOUR,
    MINIMUM_PARKING_FEE
)

logger = logging.getLogger(__name__)


class ParkingFeeCalculator:

    def __init__(
        self,
        hourly_rate=PARKING_FEE_PER_HOUR,
        minimum_fee=MINIMUM_PARKING_FEE
    ):

        self.hourly_rate = hourly_rate
        self.minimum_fee = minimum_fee

    # --------------------------------------------------------
    # CONVERT TIME
    # --------------------------------------------------------

    def parse_time(self, time_value):

        if isinstance(time_value, datetime):
            return time_value

        if isinstance(time_value, str):

            return datetime.fromisoformat(
                time_value
            )

        raise ValueError(
            "Invalid parking time format."
        )

    # --------------------------------------------------------
    # CALCULATE PARKING DURATION
    # --------------------------------------------------------

    def calculate_duration(
        self,
        entry_time,
        exit_time=None
    ):

        try:

            entry = self.parse_time(entry_time)

            if exit_time is None:
                exit_time = datetime.now()

            exit_value = self.parse_time(exit_time)

            if entry.tzinfo != exit_value.tzinfo:
                raise ValueError(
                    "Entry and exit timestamps must use "
                    "matching timezone information."
                )

            duration = exit_value - entry

            if duration.total_seconds() < 0:

                raise ValueError(
                    "Exit time cannot be earlier than entry time."
                )

            return duration

        except Exception as error:

            logger.exception(
                "Duration calculation failed: %s",
                error
            )

            raise

    # --------------------------------------------------------
    # GET DURATION IN MINUTES
    # --------------------------------------------------------

    def duration_in_minutes(
        self,
        entry_time,
        exit_time=None
    ):

        duration = self.calculate_duration(
            entry_time,
            exit_time
        )

        return round(
            duration.total_seconds() / 60,
            2
        )

    # --------------------------------------------------------
    # GET DURATION IN HOURS
    # --------------------------------------------------------

    def duration_in_hours(
        self,
        entry_time,
        exit_time=None
    ):

        duration = self.calculate_duration(
            entry_time,
            exit_time
        )

        return round(
            duration.total_seconds() / 3600,
            2
        )

    # --------------------------------------------------------
    # CALCULATE PARKING FEE
    # --------------------------------------------------------

    def calculate_fee(
        self,
        entry_time,
        exit_time=None
    ):

        try:

            duration = self.calculate_duration(
                entry_time,
                exit_time
            )

            total_seconds = duration.total_seconds()

            if total_seconds <= 0:
                return self.minimum_fee

            # Charge each started hour as a full hour
            billable_hours = math.ceil(
                total_seconds / 3600
            )

            fee = billable_hours * self.hourly_rate

            fee = max(
                fee,
                self.minimum_fee
            )

            logger.info(
                "Parking duration: %s hours, fee: Rs. %s",
                billable_hours,
                fee
            )

            return round(fee, 2)

        except Exception as error:

            logger.exception(
                "Parking fee calculation failed: %s",
                error
            )

            raise

    # --------------------------------------------------------
    # FORMAT PARKING DURATION
    # --------------------------------------------------------

    def format_duration(
        self,
        entry_time,
        exit_time=None
    ):

        duration = self.calculate_duration(
            entry_time,
            exit_time
        )

        total_seconds = int(
            duration.total_seconds()
        )

        days, remaining = divmod(
            total_seconds,
            86400
        )

        hours, remaining = divmod(
            remaining,
            3600
        )

        minutes, _ = divmod(
            remaining,
            60
        )

        return (
            f"{days} days, "
            f"{hours} hours, "
            f"{minutes} minutes"
        )

    # --------------------------------------------------------
    # GENERATE PARKING RECEIPT
    # --------------------------------------------------------

    def generate_receipt(
        self,
        plate_number,
        entry_time,
        exit_time=None
    ):

        try:

            if exit_time is None:
                exit_time = datetime.now()

            entry = self.parse_time(entry_time)
            exit_value = self.parse_time(exit_time)

            duration = self.format_duration(
                entry,
                exit_value
            )

            fee = self.calculate_fee(
                entry,
                exit_value
            )

            receipt = {
                "vehicle_number": plate_number,
                "entry_time": entry.strftime(
                    "%d-%m-%Y %I:%M:%S %p"
                ),
                "exit_time": exit_value.strftime(
                    "%d-%m-%Y %I:%M:%S %p"
                ),
                "parking_duration": duration,
                "hourly_rate": self.hourly_rate,
                "parking_fee": fee,
                "currency": "INR"
            }

            logger.info(
                "Parking receipt generated for %s",
                plate_number
            )

            return receipt

        except Exception as error:

            logger.exception(
                "Receipt generation failed: %s",
                error
            )

            raise

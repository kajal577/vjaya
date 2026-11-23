
"""
============================================================
VJaYa Robotics
PROJECT 07: SMART PARKING SYSTEM
File: database.py

SQLite Parking Database Management
============================================================
"""

import sqlite3
import logging

from datetime import datetime

from config import DATABASE_PATH

logger = logging.getLogger(__name__)


class ParkingDatabase:

    def __init__(self):

        self.database_path = str(DATABASE_PATH)

        self.initialize_database()

    # --------------------------------------------------------
    # DATABASE CONNECTION
    # --------------------------------------------------------

    def connect(self):

        return sqlite3.connect(
            self.database_path,
            timeout=10
        )

    # --------------------------------------------------------
    # INITIALIZE DATABASE
    # --------------------------------------------------------

    def initialize_database(self):

        try:

            with self.connect() as connection:

                cursor = connection.cursor()

                # Vehicle parking records
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS vehicles (

                        id INTEGER PRIMARY KEY AUTOINCREMENT,

                        plate_number TEXT NOT NULL,

                        entry_time TEXT NOT NULL,

                        exit_time TEXT,

                        parking_slot TEXT,

                        status TEXT NOT NULL DEFAULT 'PARKED',

                        entry_image TEXT,

                        exit_image TEXT,

                        parking_fee REAL DEFAULT 0

                    )
                """)

                # Parking history
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS parking_history (

                        id INTEGER PRIMARY KEY AUTOINCREMENT,

                        vehicle_id INTEGER NOT NULL,

                        plate_number TEXT NOT NULL,

                        action TEXT NOT NULL,

                        event_time TEXT NOT NULL,

                        details TEXT,

                        FOREIGN KEY(vehicle_id)
                        REFERENCES vehicles(id)

                    )
                """)

                # Parking slots
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS parking_slots (

                        slot_id TEXT PRIMARY KEY,

                        is_occupied INTEGER DEFAULT 0,

                        vehicle_id INTEGER,

                        FOREIGN KEY(vehicle_id)
                        REFERENCES vehicles(id)

                    )
                """)

                connection.commit()

            logger.info(
                "Parking database initialized."
            )

            return True

        except sqlite3.Error as error:

            logger.exception(
                "Database initialization failed: %s",
                error
            )

            return False

    # --------------------------------------------------------
    # REGISTER VEHICLE ENTRY
    # --------------------------------------------------------

    def register_entry(
        self,
        plate_number,
        parking_slot=None,
        entry_image=None
    ):

        try:

            current_time = datetime.now().isoformat(
                timespec="seconds"
            )

            with self.connect() as connection:

                cursor = connection.cursor()

                # Prevent duplicate active entries
                cursor.execute("""
                    SELECT id
                    FROM vehicles
                    WHERE plate_number = ?
                    AND status = 'PARKED'
                """, (plate_number,))

                existing = cursor.fetchone()

                if existing:

                    logger.warning(
                        "Vehicle already parked: %s",
                        plate_number
                    )

                    return None

                # Create vehicle record
                cursor.execute("""
                    INSERT INTO vehicles (

                        plate_number,
                        entry_time,
                        parking_slot,
                        status,
                        entry_image

                    )
                    VALUES (?, ?, ?, 'PARKED', ?)
                """, (
                    plate_number,
                    current_time,
                    parking_slot,
                    entry_image
                ))

                vehicle_id = cursor.lastrowid

                # Update parking slot
                if parking_slot:

                    cursor.execute("""
                        UPDATE parking_slots
                        SET is_occupied = 1,
                            vehicle_id = ?
                        WHERE slot_id = ?
                    """, (
                        vehicle_id,
                        parking_slot
                    ))

                # Record entry history
                cursor.execute("""
                    INSERT INTO parking_history (

                        vehicle_id,
                        plate_number,
                        action,
                        event_time,
                        details

                    )
                    VALUES (?, ?, 'ENTRY', ?, ?)
                """, (
                    vehicle_id,
                    plate_number,
                    current_time,
                    f"Vehicle entered slot {parking_slot}"
                ))

                connection.commit()

            logger.info(
                "Vehicle entry recorded: %s",
                plate_number
            )

            return vehicle_id

        except sqlite3.Error as error:

            logger.exception(
                "Vehicle entry registration failed: %s",
                error
            )

            return None

    # --------------------------------------------------------
    # REGISTER VEHICLE EXIT
    # --------------------------------------------------------

    def register_exit(
        self,
        plate_number,
        parking_fee=0,
        exit_image=None
    ):

        try:

            current_time = datetime.now().isoformat(
                timespec="seconds"
            )

            with self.connect() as connection:

                cursor = connection.cursor()

                cursor.execute("""
                    SELECT id, parking_slot
                    FROM vehicles
                    WHERE plate_number = ?
                    AND status = 'PARKED'
                    ORDER BY entry_time DESC
                    LIMIT 1
                """, (plate_number,))

                vehicle = cursor.fetchone()

                if vehicle is None:

                    logger.warning(
                        "No active parking record for: %s",
                        plate_number
                    )

                    return False

                vehicle_id, parking_slot = vehicle

                cursor.execute("""
                    UPDATE vehicles

                    SET exit_time = ?,
                        status = 'EXITED',
                        parking_fee = ?,
                        exit_image = ?

                    WHERE id = ?
                """, (
                    current_time,
                    parking_fee,
                    exit_image,
                    vehicle_id
                ))

                # Free parking slot
                if parking_slot:

                    cursor.execute("""
                        UPDATE parking_slots

                        SET is_occupied = 0,
                            vehicle_id = NULL

                        WHERE slot_id = ?
                        AND vehicle_id = ?
                    """, (
                        parking_slot,
                        vehicle_id
                    ))

                # Record exit history
                cursor.execute("""
                    INSERT INTO parking_history (

                        vehicle_id,
                        plate_number,
                        action,
                        event_time,
                        details

                    )
                    VALUES (?, ?, 'EXIT', ?, ?)
                """, (
                    vehicle_id,
                    plate_number,
                    current_time,
                    f"Parking fee: Rs. {parking_fee}"
                ))

                connection.commit()

            logger.info(
                "Vehicle exit recorded: %s",
                plate_number
            )

            return True

        except sqlite3.Error as error:

            logger.exception(
                "Vehicle exit registration failed: %s",
                error
            )

            return False

    # --------------------------------------------------------
    # CHECK ACTIVE VEHICLE
    # --------------------------------------------------------

    def is_vehicle_parked(self, plate_number):

        try:

            with self.connect() as connection:

                cursor = connection.cursor()

                cursor.execute("""
                    SELECT EXISTS(
                        SELECT 1
                        FROM vehicles
                        WHERE plate_number = ?
                        AND status = 'PARKED'
                    )
                """, (plate_number,))

                return bool(cursor.fetchone()[0])

        except sqlite3.Error as error:

            logger.exception(
                "Vehicle status check failed: %s",
                error
            )

            return False

    # --------------------------------------------------------
    # GET ACTIVE VEHICLES
    # --------------------------------------------------------

    def get_parked_vehicles(self):

        try:

            with self.connect() as connection:

                cursor = connection.cursor()

                cursor.execute("""
                    SELECT
                        id,
                        plate_number,
                        entry_time,
                        parking_slot,
                        entry_image

                    FROM vehicles

                    WHERE status = 'PARKED'

                    ORDER BY entry_time DESC
                """)

                return cursor.fetchall()

        except sqlite3.Error as error:

            logger.exception(
                "Active vehicle retrieval failed: %s",
                error
            )

            return []

    # --------------------------------------------------------
    # GET VEHICLE RECORD
    # --------------------------------------------------------

    def get_vehicle(self, plate_number):

        try:

            with self.connect() as connection:

                cursor = connection.cursor()

                cursor.execute("""
                    SELECT *
                    FROM vehicles
                    WHERE plate_number = ?
                    ORDER BY entry_time DESC
                    LIMIT 1
                """, (plate_number,))

                return cursor.fetchone()

        except sqlite3.Error as error:

            logger.exception(
                "Vehicle retrieval failed: %s",
                error
            )

            return None

    # --------------------------------------------------------
    # GET PARKING HISTORY
    # --------------------------------------------------------

    def get_parking_history(self, limit=100):

        try:

            with self.connect() as connection:

                cursor = connection.cursor()

                cursor.execute("""
                    SELECT
                        id,
                        plate_number,
                        action,
                        event_time,
                        details

                    FROM parking_history

                    ORDER BY id DESC

                    LIMIT ?
                """, (limit,))

                return cursor.fetchall()

        except sqlite3.Error as error:

            logger.exception(
                "Parking history retrieval failed: %s",
                error
            )

            return []

    # --------------------------------------------------------
    # INITIALIZE PARKING SLOTS
    # --------------------------------------------------------

    def initialize_slots(self, slot_names):

        try:

            with self.connect() as connection:

                cursor = connection.cursor()

                for slot in slot_names:

                    cursor.execute("""
                        INSERT OR IGNORE INTO parking_slots (
                            slot_id,
                            is_occupied
                        )
                        VALUES (?, 0)
                    """, (slot,))

                connection.commit()

            return True

        except sqlite3.Error as error:

            logger.exception(
                "Parking slot initialization failed: %s",
                error
            )

            return False

    # --------------------------------------------------------
    # GET PARKING SLOT STATUS
    # --------------------------------------------------------

    def get_slot_status(self):

        try:

            with self.connect() as connection:

                cursor = connection.cursor()

                cursor.execute("""
                    SELECT
                        slot_id,
                        is_occupied,
                        vehicle_id

                    FROM parking_slots

                    ORDER BY slot_id
                """)

                return cursor.fetchall()

        except sqlite3.Error as error:

            logger.exception(
                "Parking slot retrieval failed: %s",
                error
            )

            return []

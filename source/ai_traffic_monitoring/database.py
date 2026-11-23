
import sqlite3
import json
from datetime import datetime

from config import DATABASE_PATH


class TrafficDatabase:

    def __init__(self):

        self.connection = sqlite3.connect(
            str(DATABASE_PATH),
            check_same_thread=False
        )

        self.create_tables()

    def create_tables(self):

        cursor = self.connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS traffic_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                total_vehicles INTEGER,
                cars INTEGER,
                motorcycles INTEGER,
                buses INTEGER,
                trucks INTEGER,
                congestion TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vehicle_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                track_id INTEGER,
                vehicle_type TEXT,
                confidence REAL
            )
        """)

        self.connection.commit()

    def save_statistics(self, statistics, congestion):

        cursor = self.connection.cursor()

        cursor.execute("""
            INSERT INTO traffic_records (
                timestamp,
                total_vehicles,
                cars,
                motorcycles,
                buses,
                trucks,
                congestion
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            statistics.get("vehicles_present", 0),
            statistics.get("cars", 0),
            statistics.get("motorcycles", 0),
            statistics.get("buses", 0),
            statistics.get("trucks", 0),
            congestion
        ))

        self.connection.commit()

    def save_vehicle_event(self, detection):

        cursor = self.connection.cursor()

        cursor.execute("""
            INSERT INTO vehicle_events (
                timestamp,
                track_id,
                vehicle_type,
                confidence
            )
            VALUES (?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            detection.get("track_id"),
            detection.get("vehicle_type"),
            detection.get("confidence", 0)
        ))

        self.connection.commit()

    def get_recent_records(self, limit=50):

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT * FROM traffic_records
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))

        return cursor.fetchall()

    def close(self):

        if self.connection:
            self.connection.close()

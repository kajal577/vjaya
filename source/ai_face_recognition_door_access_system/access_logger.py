import sqlite3
from datetime import datetime
from pathlib import Path

from config import ACCESS_DATABASE


class AccessLogger:

    def __init__(self):

        database_path = Path(ACCESS_DATABASE)

        database_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.connection = sqlite3.connect(
            str(database_path),
            check_same_thread=False
        )

        self.create_table()

    def create_table(self):

        query = """
        CREATE TABLE IF NOT EXISTS access_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT,
            user_id TEXT,
            status TEXT NOT NULL,
            access_method TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
        """

        self.connection.execute(query)
        self.connection.commit()

    def log_access(
        self,
        user_name,
        user_id,
        status,
        access_method="FACE"
    ):

        timestamp = datetime.now().isoformat(
            timespec="seconds"
        )

        query = """
        INSERT INTO access_logs
        (user_name, user_id, status, access_method, timestamp)
        VALUES (?, ?, ?, ?, ?)
        """

        self.connection.execute(
            query,
            (
                user_name,
                str(user_id) if user_id is not None else None,
                status,
                access_method,
                timestamp
            )
        )

        self.connection.commit()

        print(
            f"[LOG] {status}: {user_name} "
            f"({access_method}) at {timestamp}"
        )

    def get_recent_logs(self, limit=20):

        cursor = self.connection.execute(
            """
            SELECT * FROM access_logs
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        )

        return cursor.fetchall()

    def close(self):

        if self.connection:
            self.connection.close()
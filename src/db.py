import sqlite3
from pathlib import Path

DB_PATH = Path("installations.db")


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS installations (
                id INTEGER PRIMARY KEY,
                package TEXT,
                method TEXT,
                success INTEGER,
                duration INTEGER,
                log TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        )


def record_install(package, method, success, duration, log):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO installations (package, method, success, duration, log)
            VALUES (?, ?, ?, ?, ?)
        """,
            (package, method, int(success), duration, log),
        )

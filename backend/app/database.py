
import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent.parent / "patchops.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS devices (
                device_id TEXT PRIMARY KEY,
                hostname TEXT NOT NULL,
                operating_system TEXT NOT NULL,
                os_version TEXT NOT NULL,
                os_release TEXT NOT NULL,
                architecture TEXT NOT NULL,
                python_version TEXT NOT NULL
            )
        """)
        connection.commit()

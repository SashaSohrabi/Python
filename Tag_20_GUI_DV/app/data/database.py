# pyright: strict
import sqlite3
from pathlib import Path

from ..constants.constants import STATUS_COMPLETED, STATUS_OPEN
from .infrastructure import SAMPLE_TICKETS


def open_database_connection(db_path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(db_path, timeout=5.0)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database(db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)

    connection = open_database_connection(db_path)

    try:
        connection.execute("BEGIN IMMEDIATE")
        connection.execute(f"""
            CREATE TABLE IF NOT EXISTS tickets (
                id     INTEGER PRIMARY KEY AUTOINCREMENT,
                title    TEXT NOT NULL CHECK (length(trim(title)) > 0),
                status   TEXT NOT NULL DEFAULT '{STATUS_OPEN}'
                        CHECK (status IN ('{STATUS_OPEN}', '{STATUS_COMPLETED}')),
                priority INTEGER NOT NULL CHECK (priority BETWEEN 1 AND 3)
                )
            """)

        if connection.execute("SELECT 1 FROM tickets LIMIT 1").fetchone() is None:
            connection.executemany(
                "INSERT INTO tickets (title, status, priority) VALUES (?, ?, ?)",
                SAMPLE_TICKETS,
            )

        connection.commit()
    except sqlite3.Error:
        connection.rollback()
        raise
    finally:
        connection.close()

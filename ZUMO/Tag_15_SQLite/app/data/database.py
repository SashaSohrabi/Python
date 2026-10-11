# pyright: strict
"""Database connections and the shared table schema."""

import sqlite3
from pathlib import Path


def open_database_connection(db: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(db)
    # Allow accessing query results by column name, e.g. row["name"].
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database(db: Path) -> None:
    """Create the server table if it does not exist."""
    conn = open_database_connection(db)
    try:
        conn.execute("BEGIN")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS server (
                id        INTEGER PRIMARY KEY,
                server_type TEXT   NOT NULL,
                name      TEXT    NOT NULL UNIQUE,
                role      TEXT    NOT NULL,
                ip        TEXT    NOT NULL,
                cpu       INTEGER NOT NULL,
                status    TEXT    NOT NULL,
                framework TEXT,
                since     TEXT
            )
        """)
        conn.commit()
    except sqlite3.Error:
        conn.rollback()
        raise
    finally:
        conn.close()

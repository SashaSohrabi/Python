# pyright: strict
"""Database connections and the shared table schema."""

import sqlite3
from pathlib import Path


def open_database_connection(db: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database(db: Path) -> None:
    """Create the server table and migrate legacy column names and roles."""
    conn = open_database_connection(db)
    try:
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
        # Upgrade databases created before the English column names were used.
        columns = {
            row["name"] for row in conn.execute("PRAGMA table_info(server)")
        }
        for old_name, new_name in (
            ("klasse", "server_type"),
            ("rolle", "role"),
            ("seit", "since"),
        ):
            if old_name in columns and new_name not in columns:
                conn.execute(
                    f"ALTER TABLE server RENAME COLUMN {old_name} TO {new_name}"
                )
                columns.remove(old_name)
                columns.add(new_name)
        conn.execute(
            "UPDATE server SET role = ? WHERE role = ?", ("Database", "Datenbank")
        )
        conn.commit()
    finally:
        conn.close()

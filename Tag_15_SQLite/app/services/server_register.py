# pyright: strict
"""SQL queries; every operation reliably closes its connection."""

import sqlite3
from collections.abc import Sequence
from pathlib import Path
from typing import Final

from ..data.database import open_database_connection
from ..models.backup_server import BackupServer
from ..models.server import Server
from ..models.validation import (
    get_integer_field,
    get_text_field,
    validate_cpu_load,
)
from ..models.web_server import WebServer

SERVER_TYPES: Final[dict[str, type[Server]]] = {
    "Server": Server, "WebServer": WebServer, "BackupServer": BackupServer,
}


class ServerRegister:
    def __init__(self, db: Path) -> None:
        self.db = db

    def insert_missing_servers(self, servers: Sequence[Server]) -> int:
        """Insert servers with new names, preserving existing rows; return the count."""
        conn = open_database_connection(self.db)
        inserted_count = 0
        try:
            cursor = conn.cursor()
            for server in servers:
                existing = cursor.execute(
                    "SELECT id FROM server WHERE name = ?", (server.name,)
                ).fetchone()
                if existing is not None:
                    continue
                row = server.to_row()
                columns = ", ".join(row.keys())
                placeholders = ", ".join("?" for _ in row)
                cursor.execute(
                    f"INSERT INTO server ({columns}) VALUES ({placeholders})",
                    tuple(row.values()),
                )
                inserted_count += cursor.rowcount
            conn.commit()
            return inserted_count
        finally:
            conn.close()

    def fetch_rows(
        self, sql: str, parameters: tuple[object, ...] = (),
    ) -> list[dict[str, object]]:
        conn = open_database_connection(self.db)
        try:
            rows: list[sqlite3.Row] = conn.execute(sql, parameters).fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

    def fetch_server_rows(self) -> list[dict[str, object]]:
        return self.fetch_rows("SELECT * FROM server ORDER BY id")

    def load_servers(self) -> list[Server]:
        servers: list[Server] = []
        for row in self.fetch_server_rows():
            row.pop("id", None)
            server_class = SERVER_TYPES[get_text_field(row, "server_type")]
            servers.append(server_class.from_row(row))
        return servers

    def search_by_min_cpu(self, minimum_cpu: int) -> list[str]:
        rows = self.fetch_rows(
            "SELECT name, server_type, cpu FROM server WHERE cpu >= ? "
            "ORDER BY cpu DESC, id ASC", (validate_cpu_load(minimum_cpu),),
        )
        return [
            f"{get_text_field(row, 'name')} ({get_text_field(row, 'server_type')}, "
            f"CPU {get_integer_field(row, 'cpu')} %)" for row in rows
        ]

    def compare_role_and_cpu_filters(self) -> dict[str, list[str]]:
        """Compare AND/OR results for role Database and CPU load of at least 80%."""
        and_rows = self.fetch_rows(
            "SELECT name FROM server WHERE role = ? AND cpu >= ? ORDER BY id",
            ("Database", 80),
        )
        or_rows = self.fetch_rows(
            "SELECT name FROM server WHERE role = ? OR cpu >= ? ORDER BY id",
            ("Database", 80),
        )
        return {
            "AND": [get_text_field(row, "name") for row in and_rows],
            "OR": [get_text_field(row, "name") for row in or_rows],
        }

    def set_cpu_load(self, name: str, cpu_load: int) -> int:
        """Set CPU load by name and return matched rows, including unchanged values."""
        validate_cpu_load(cpu_load)
        conn = open_database_connection(self.db)
        try:
            cursor = conn.execute(
                "UPDATE server SET cpu = ? WHERE name = ?", (cpu_load, name),
            )
            matched_count = cursor.rowcount
            conn.commit()
            return matched_count
        finally:
            conn.close()

    def count_by_server_type(self) -> dict[str, int]:
        rows = self.fetch_rows(
            "SELECT server_type, COUNT(*) AS count FROM server "
            "GROUP BY server_type ORDER BY server_type"
        )
        return {
            get_text_field(row, "server_type"): get_integer_field(row, "count")
            for row in rows
        }

    def fetch_highest_cpu_row(self) -> dict[str, object] | None:
        """Return the name and CPU load of the busiest server, or None if empty."""
        conn = open_database_connection(self.db)
        try:
            # For equal loads, the lower ID comes first (web-02 before db-01).
            row: sqlite3.Row | None = conn.execute(
                "SELECT name, cpu FROM server ORDER BY cpu DESC, id ASC"
            ).fetchone()
            return dict(row) if row is not None else None
        finally:
            conn.close()

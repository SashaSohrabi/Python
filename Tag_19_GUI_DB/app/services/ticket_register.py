# pyright: strict
"""All ticket queries and writes, following Tag_15_SQLite's register structure."""

import sqlite3
from contextlib import closing
from pathlib import Path

from ..constants.ticket_status import STATUS_COMPLETED, STATUS_OPEN
from ..data.database import open_database_connection
from ..models.validation import ticket_from_row, validate_priority, validate_title
from ..types.ticket_types import Ticket


class TicketRegister:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path

    def get_all_tickets(self) -> list[Ticket]:
        with closing(open_database_connection(self.db_path)) as connection:
            rows: list[sqlite3.Row] = connection.execute(
                "SELECT id, title, status, priority FROM tickets ORDER BY id"
            ).fetchall()
        return [ticket_from_row(row) for row in rows]

    def create_ticket(self, title: str, priority: int) -> int:
        cleaned = validate_title(title)
        priority = validate_priority(priority)
        with closing(open_database_connection(self.db_path)) as connection:
            cursor = connection.execute(
                "INSERT INTO tickets (title, status, priority) VALUES (?, ?, ?)",
                (cleaned, STATUS_OPEN, priority),
            )
            new_id = cursor.lastrowid
            if new_id is None:
                raise RuntimeError("SQLite did not return a ticket ID.")

            connection.commit()

        return new_id

    def toggle_ticket_status(self, ticket_id: int) -> bool:
        if isinstance(ticket_id, bool) or ticket_id < 1:
            raise ValueError("Ticket ID must be a positive integer.")
        with closing(open_database_connection(self.db_path)) as connection:
            cursor = connection.execute(
                """
                UPDATE tickets
                SET status = CASE WHEN status = ? THEN ? ELSE ? END
                WHERE id = ?
                """,
                (STATUS_OPEN, STATUS_COMPLETED, STATUS_OPEN, ticket_id),
            )

            connection.commit()

            return cursor.rowcount > 0

    def delete_ticket(self, ticket_id: int) -> bool:
        if isinstance(ticket_id, bool) or ticket_id < 1:
            raise ValueError("Ticket ID must be a positive integer.")
        with closing(open_database_connection(self.db_path)) as connection:
            cursor = connection.execute(
                "DELETE FROM tickets WHERE id = ?", (ticket_id,)
            )

            connection.commit()

            return cursor.rowcount > 0

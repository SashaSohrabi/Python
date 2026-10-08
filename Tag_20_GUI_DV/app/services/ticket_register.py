# pyright: strict
import sqlite3
from contextlib import closing
from pathlib import Path

from ..constants.ticket_status import FILTER_ALL, STATUS_COMPLETED, STATUS_OPEN
from ..data.database import open_database_connection
from ..models.validation import (
    ticket_from_row,
    validate_filter,
    validate_priority,
    validate_status,
    validate_title,
)
from ..types.ticket_types import Ticket, TicketFilter, TicketStatus


class TicketRegister:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path

    def get_all_tickets(self) -> list[Ticket]:
        return self.get_filtered_tickets()

    def get_filtered_tickets(self, status: TicketFilter = FILTER_ALL) -> list[Ticket]:
        status = validate_filter(status)
        with closing(open_database_connection(self.db_path)) as connection:
            query = "SELECT id, title, status, priority FROM tickets"
            parameters: tuple[str, ...] = ()
            if status != FILTER_ALL:
                query += " WHERE status = ?"
                parameters = (status,)
            query += " ORDER BY priority DESC, id"
            rows: list[sqlite3.Row] = connection.execute(query, parameters).fetchall()
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

    def change_ticket_status(self, ticket_id: int, status: TicketStatus) -> bool:
        if isinstance(ticket_id, bool) or ticket_id < 1:
            raise ValueError("Ticket ID must be a positive integer.")
        status = validate_status(status)
        with closing(open_database_connection(self.db_path)) as connection:
            cursor = connection.execute(
                "UPDATE tickets SET status = ? WHERE id = ?", (status, ticket_id)
            )
            connection.commit()
            return cursor.rowcount > 0

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

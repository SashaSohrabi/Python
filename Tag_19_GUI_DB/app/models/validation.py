# pyright: strict
"""Validate form input and untrusted values returned by SQLite."""

import sqlite3

from ..constants.settings import MAX_PRIORITY, MIN_PRIORITY
from ..constants.ticket_status import STATUS_COMPLETED, STATUS_OPEN
from ..types.ticket_types import Ticket, TicketStatus


def validate_title(title: str) -> str:
    cleaned = title.strip()
    if not cleaned:
        raise ValueError("Please enter a title.")
    return cleaned


def validate_priority(priority: object) -> int:
    if not isinstance(priority, int) or isinstance(priority, bool):
        raise TypeError("Priority must be a whole number.")
    if not MIN_PRIORITY <= priority <= MAX_PRIORITY:
        raise ValueError(f"Priority must be between {MIN_PRIORITY} and {MAX_PRIORITY}.")
    return priority


def parse_priority(text: str) -> int:
    try:
        priority = int(text.strip())
    except ValueError as error:
        raise ValueError("Please enter a whole number for priority.") from error
    return validate_priority(priority)


def _integer(row: sqlite3.Row, name: str) -> int:
    value: object = row[name]
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"Database column '{name}' must contain a whole number.")
    return value


def _text(row: sqlite3.Row, name: str) -> str:
    value: object = row[name]
    if not isinstance(value, str):
        raise TypeError(f"Database column '{name}' must contain text.")
    return value


def _status(row: sqlite3.Row) -> TicketStatus:
    value = _text(row, "status")
    if value == STATUS_OPEN:
        return STATUS_OPEN
    if value == STATUS_COMPLETED:
        return STATUS_COMPLETED
    raise ValueError(f"Unknown ticket status: {value!r}")


def ticket_from_row(row: sqlite3.Row) -> Ticket:
    return {
        "id": _integer(row, "id"),
        "title": validate_title(_text(row, "title")),
        "status": _status(row),
        "priority": validate_priority(_integer(row, "priority")),
    }

# pyright: strict
import sqlite3

from ..constants.constants import (
    FILTER_ALL,
    MAX_PRIORITY,
    MIN_PRIORITY,
    STATUS_COMPLETED,
    STATUS_OPEN,
)
from ..types.types import Ticket, TicketFilter, TicketStatus


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


def validate_status(status: str) -> TicketStatus:
    if status == STATUS_OPEN:
        return STATUS_OPEN
    if status == STATUS_COMPLETED:
        return STATUS_COMPLETED
    raise ValueError(f"Unknown ticket status: {status!r}")


def validate_filter(status: str) -> TicketFilter:
    if status == FILTER_ALL:
        return FILTER_ALL
    return validate_status(status)


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
    return validate_status(_text(row, "status"))


def ticket_from_row(row: sqlite3.Row) -> Ticket:
    return {
        "id": _integer(row, "id"),
        "title": validate_title(_text(row, "title")),
        "status": _status(row),
        "priority": validate_priority(_integer(row, "priority")),
    }

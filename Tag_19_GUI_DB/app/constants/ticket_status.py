# pyright: strict
"""Literal ticket status constants shared by the database and UI."""

from typing import Final

from ..types.ticket_types import TicketStatus

STATUS_OPEN: Final[TicketStatus] = "open"
STATUS_COMPLETED: Final[TicketStatus] = "completed"

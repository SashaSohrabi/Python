# pyright: strict
from typing import TypedDict

from .ticket_types import Ticket, TicketFilter


class TicketListState(TypedDict):
    tickets: list[Ticket]
    status_filter: TicketFilter
    revision: int
    message: str
    error: str | None


class TicketFormState(TypedDict):
    title: str
    priority: str
    title_error: str | None
    priority_error: str | None
    save_error: str | None


class DeleteTicketState(TypedDict):
    ticket: Ticket | None
    error: str | None

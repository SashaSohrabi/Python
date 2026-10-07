# pyright: strict
"""Typed dictionary keys for the list, form and delete dialog."""

from typing import TypedDict

from .ticket_types import Ticket


class TicketListState(TypedDict):
    tickets: list[Ticket]
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

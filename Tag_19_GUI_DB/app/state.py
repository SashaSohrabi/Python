# pyright: strict
"""Factories and loading logic for ticket-related UI state."""

import sqlite3

from .services.ticket_register import TicketRegister
from .types.state_types import DeleteTicketState, TicketFormState, TicketListState
from .types.ticket_types import Ticket


class State:
    def __init__(self, register: TicketRegister) -> None:
        self.register = register

    def create_ticket_form_state(self, priority: str = "2") -> TicketFormState:
        return {
            "title": "",
            "priority": priority,
            "title_error": None,
            "priority_error": None,
            "save_error": None,
        }

    def create_delete_ticket_state(
        self, ticket: Ticket | None = None
    ) -> DeleteTicketState:
        return {"ticket": ticket, "error": None}

    def load_ticket_state(
        self,
        previous: TicketListState | None = None,
        message: str = "",
    ) -> TicketListState:
        try:
            return {
                "tickets": self.register.get_all_tickets(),
                "message": message,
                "error": None,
            }
        except (sqlite3.Error, TypeError, ValueError) as error:
            return {
                "tickets": previous["tickets"] if previous is not None else [],
                "message": message,
                "error": f"Could not load tickets: {error}",
            }

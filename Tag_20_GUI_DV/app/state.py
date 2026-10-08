# pyright: strict
import sqlite3

from .constants.ticket_status import FILTER_ALL
from .services.ticket_register import TicketRegister
from .types.state_types import DeleteTicketState, TicketFormState, TicketListState
from .types.ticket_types import Ticket, TicketFilter


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
        status_filter: TicketFilter | None = None,
    ) -> TicketListState:
        selected_filter = status_filter
        if selected_filter is None:
            selected_filter = (
                previous["status_filter"] if previous is not None else FILTER_ALL
            )

        revision = previous["revision"] + 1 if previous is not None else 0
        try:
            return {
                "tickets": self.register.get_filtered_tickets(selected_filter),
                "status_filter": selected_filter,
                "revision": revision,
                "message": message,
                "error": None,
            }
        except (sqlite3.Error, TypeError, ValueError) as error:
            return {
                "tickets": previous["tickets"] if previous is not None else [],
                "status_filter": (
                    previous["status_filter"]
                    if previous is not None
                    else selected_filter
                ),
                "revision": revision,
                "message": "",
                "error": f"Could not load tickets: {error}",
            }

# pyright: strict
"""Compose declarative components; SQL lives entirely in TicketRegister."""

import sqlite3

import flet as ft

from ..components.delete_ticket_dialog import build_delete_dialog
from ..components.ticket_form import TicketForm
from ..components.ticket_table import TicketTable
from ..constants.settings import APP_TITLE, PAGE_PADDING
from ..services.ticket_register import TicketRegister
from ..state import State
from ..types.flet_types import use_state
from ..types.ticket_types import Ticket


@ft.component
def TicketApp(register: TicketRegister) -> ft.Container:
    state = State(register)
    tickets_state, set_tickets_state = use_state(state.load_ticket_state)
    deletion, set_deletion = use_state(state.create_delete_ticket_state)

    def reload_tickets(message: str) -> None:
        set_tickets_state(lambda previous: state.load_ticket_state(previous, message))

    def reload() -> None:
        reload_tickets("Tickets reloaded from the database.")

    def create_ticket(title: str, priority: int) -> str | None:
        try:
            new_id = register.create_ticket(title, priority)
        except (sqlite3.Error, TypeError, ValueError, RuntimeError) as error:
            return f"Could not save ticket: {error}"
        print(f"New ticket: ID {new_id} (assigned by SQLite)")
        reload_tickets(f"Ticket {new_id} saved.")
        return None

    def request_delete(ticket: Ticket) -> None:
        set_deletion(state.create_delete_ticket_state(ticket=ticket))

    def toggle_status(ticket: Ticket) -> None:
        try:
            updated = register.toggle_ticket_status(ticket["id"])
        except (sqlite3.Error, ValueError) as error:
            error_message = f"Could not update ticket status: {error}"
            set_tickets_state(
                lambda previous: {**previous, "message": "", "error": error_message}
            )
            return
        message = (
            f"Ticket {ticket['id']} status updated."
            if updated
            else f"Ticket {ticket['id']} has already been deleted."
        )
        reload_tickets(message)

    def cancel_delete() -> None:
        set_deletion(state.create_delete_ticket_state())

    def confirm_delete() -> None:
        ticket = deletion["ticket"]
        if ticket is None:
            return
        try:
            deleted = register.delete_ticket(ticket["id"])
        except (sqlite3.Error, ValueError) as error:
            set_deletion({**deletion, "error": f"Could not delete ticket: {error}"})
            return
        set_deletion(state.create_delete_ticket_state())
        message = (
            f"Ticket {ticket['id']} deleted."
            if deleted
            else f"Ticket {ticket['id']} has already been deleted."
        )
        reload_tickets(message)

    ft.use_dialog(build_delete_dialog(deletion, confirm_delete, cancel_delete))

    return ft.Container(
        padding=PAGE_PADDING,
        expand=True,
        content=ft.Column(
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            spacing=16,
            controls=[
                ft.Text(APP_TITLE, size=28, weight=ft.FontWeight.BOLD),
                ft.Text(f"{len(tickets_state['tickets'])} tickets"),
                ft.Button("Reload", icon=ft.Icons.REFRESH, on_click=reload),
                ft.Text(
                    tickets_state["message"],
                    color=ft.Colors.PRIMARY,
                    visible=bool(tickets_state["message"]),
                ),
                ft.Text(
                    tickets_state["error"] or "",
                    color=ft.Colors.ERROR,
                    visible=tickets_state["error"] is not None,
                ),
                TicketTable(tickets_state["tickets"], request_delete, toggle_status),
                ft.Divider(),
                TicketForm(create_ticket, state),
            ],
        ),
    )


def show_ticket_app(page: ft.Page, register: TicketRegister) -> None:
    page.title = APP_TITLE
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.window.width = 840
    page.window.height = 920
    page.render(TicketApp, register)

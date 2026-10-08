# pyright: strict
import sqlite3

import flet as ft

from ..components.delete_ticket_dialog import build_delete_dialog
from ..components.ticket_detail_dialog import build_detail_dialog
from ..components.ticket_form import TicketForm
from ..components.ticket_list import TicketList
from ..constants.settings import APP_TITLE, PAGE_PADDING
from ..constants.ticket_status import FILTER_ALL, STATUS_COMPLETED, STATUS_OPEN
from ..models.validation import validate_filter
from ..services.ticket_register import TicketRegister
from ..state import State
from ..types.flet_types import use_state
from ..types.state_types import TicketListState
from ..types.ticket_types import Ticket, TicketFilter


@ft.component
def TicketApp(register: TicketRegister, page: ft.Page) -> ft.Container:
    state = State(register)

    def reload_tickets(
        previous: TicketListState | None = None,
        message: str = "",
        status_filter: TicketFilter | None = None,
    ) -> TicketListState:
        return state.load_ticket_state(previous, message, status_filter)

    # Start and every subsequent action go through reload_tickets.
    tickets_state, set_tickets_state = use_state(reload_tickets)

    def feedback(text: str, ok: bool = True) -> None:
        page.show_dialog(
            ft.SnackBar(
                content=ft.Text(text, color=ft.Colors.WHITE),
                bgcolor=ft.Colors.GREEN_700 if ok else ft.Colors.RED_400,
            )
        )

    def refresh(
        message: str = "",
        status_filter: TicketFilter | None = None,
        ok: bool = True,
    ) -> None:
        loaded = reload_tickets(tickets_state, message, status_filter)
        set_tickets_state(loaded)
        if loaded["error"] is not None:
            feedback(loaded["error"], False)
        elif message:
            feedback(message, ok)

    def reload() -> None:
        refresh("Tickets reloaded from the database.")

    def change_filter(event: ft.Event[ft.Dropdown]) -> None:
        try:
            selected = validate_filter(event.control.value or FILTER_ALL)
        except ValueError as error:
            feedback(str(error), False)
            return
        refresh(status_filter=selected)

    def create_ticket(title: str, priority: int) -> str | None:
        try:
            new_id = register.create_ticket(title, priority)
        except (sqlite3.Error, TypeError, ValueError, RuntimeError) as error:
            return f"Could not save ticket: {error}"
        refresh(f"Ticket {new_id} saved.")
        return None

    def close_dialog() -> None:
        page.pop_dialog()

    def request_delete(ticket: Ticket) -> None:
        error_text = ft.Text("", color=ft.Colors.ERROR, visible=False)

        def confirm_delete() -> None:
            try:
                deleted = register.delete_ticket(ticket["id"])
            except (sqlite3.Error, ValueError) as error:
                error_text.value = f"Could not delete ticket: {error}"
                error_text.visible = True
                error_text.update()
                return
            close_dialog()
            message = (
                f"Ticket {ticket['id']} deleted."
                if deleted
                else f"Ticket {ticket['id']} has already been deleted."
            )
            refresh(message, ok=deleted)

        dialog = build_delete_dialog(
            state.create_delete_ticket_state(ticket),
            confirm_delete,
            close_dialog,
            error_text,
        )
        if dialog is not None:
            page.show_dialog(dialog)

    def toggle_ticket_status(ticket: Ticket) -> None:
        try:
            updated = register.toggle_ticket_status(ticket["id"])
        except (sqlite3.Error, ValueError) as error:
            feedback(f"Could not update ticket status: {error}", False)
            return
        message = (
            f"Ticket {ticket['id']} status updated."
            if updated
            else f"Ticket {ticket['id']} has already been deleted."
        )
        refresh(message, ok=updated)

    def open_ticket(ticket: Ticket) -> None:
        error_text = ft.Text("", color=ft.Colors.ERROR, visible=False)

        def toggle_status() -> None:
            try:
                updated = register.toggle_ticket_status(ticket["id"])
            except (sqlite3.Error, ValueError) as error:
                error_text.value = f"Could not update ticket status: {error}"
                error_text.visible = True
                error_text.update()
                return
            close_dialog()
            message = (
                f"Ticket {ticket['id']} status updated."
                if updated
                else f"Ticket {ticket['id']} has already been deleted."
            )
            refresh(message, ok=updated)

        def delete_from_details() -> None:
            close_dialog()
            request_delete(ticket)

        page.show_dialog(
            build_detail_dialog(
                ticket, toggle_status, delete_from_details, close_dialog, error_text
            )
        )

    current_filter = tickets_state["status_filter"]
    return ft.Container(
        padding=PAGE_PADDING,
        expand=True,
        content=ft.Column(
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            spacing=16,
            controls=[
                ft.Container(
                    bgcolor=ft.Colors.INDIGO_900,
                    padding=20,
                    border_radius=8,
                    content=ft.Text(
                        APP_TITLE,
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE,
                    ),
                ),
                TicketForm(create_ticket, state, feedback),
                ft.Divider(),
                ft.Row(
                    wrap=True,
                    controls=[
                        ft.Button("Reload", icon=ft.Icons.REFRESH, on_click=reload),
                        ft.Dropdown(
                            key="ticket-filter",
                            label="Status",
                            width=180,
                            value=current_filter,
                            options=[
                                ft.DropdownOption(FILTER_ALL, text="All"),
                                ft.DropdownOption(STATUS_OPEN, text="Open"),
                                ft.DropdownOption(STATUS_COMPLETED, text="Completed"),
                            ],
                            on_select=change_filter,
                        ),
                    ],
                ),
                ft.Text(
                    f"{len(tickets_state['tickets'])} tickets · Filter: {current_filter}",
                    key="ticket-count",
                ),
                ft.Text(
                    tickets_state["error"] or "",
                    color=ft.Colors.ERROR,
                    visible=tickets_state["error"] is not None,
                ),
                TicketList(
                    tickets_state["tickets"],
                    open_ticket,
                    current_filter,
                    request_delete,
                    toggle_ticket_status,
                ),
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
    page.render(TicketApp, register, page)

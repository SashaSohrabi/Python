# pyright: strict
import sqlite3
from typing import cast

import flet as ft

from ..components.app_header import AppHeader
from ..components.delete_ticket_dialog import DeleteTicketDialog
from ..components.ticket_detail_dialog import TicketDetailDialog
from ..components.ticket_form import TicketForm
from ..components.ticket_list import TicketList
from ..components.ticket_toolbar import TicketToolbar
from ..constants.constants import APP_TITLE, FILTER_ALL, PAGE_PADDING
from ..models.ticket_register import TicketRegister
from ..services.validation import validate_filter
from ..types.types import Ticket, TicketFilter, TicketListState, use_state


@ft.component
def TicketApp(register: TicketRegister, page: ft.Page) -> ft.Container:
    tickets_state: TicketListState = {
        "tickets": [],
        "status_filter": FILTER_ALL,
        "revision": 0,
        "error": None,
    }

    tickets_state, set_tickets_state = use_state(tickets_state)

    detail_ticket, set_detail_ticket = use_state(cast(Ticket | None, None))

    delete_ticket, set_delete_ticket = use_state(cast(Ticket | None, None))

    def feedback(text: str, ok: bool = True) -> None:
        page.show_dialog(
            ft.SnackBar(
                content=ft.Text(text, color=ft.Colors.WHITE),
                bgcolor=ft.Colors.GREEN_700 if ok else ft.Colors.RED_400,
            )
        )

    def close_detail_dialog() -> None:
        nonlocal detail_ticket
        detail_ticket = None
        set_detail_ticket(None)

    def close_delete_dialog() -> None:
        nonlocal delete_ticket
        delete_ticket = None
        set_delete_ticket(None)

    def refresh(
        message: str = "",
        status_filter: TicketFilter | None = None,
        ok: bool = True,
    ) -> None:
        nonlocal tickets_state
        selected_filter = status_filter or tickets_state["status_filter"]
        next_state: TicketListState = {
            **tickets_state,
            "revision": tickets_state["revision"] + 1,
            "error": None,
        }
        try:
            next_state["tickets"] = register.get_filtered_tickets(selected_filter)
            next_state["status_filter"] = selected_filter
        except (sqlite3.Error, TypeError, ValueError) as load_error:
            next_state["error"] = f"Could not load tickets: {load_error}"

        # Keep callbacks in sync even if another action runs before a render.
        tickets_state = next_state
        set_tickets_state(tickets_state)
        error = tickets_state["error"]
        if error is not None:
            feedback(error, ok=False)
        elif message:
            feedback(message, ok)

    ft.on_mounted(refresh)

    # Ticket actions used by the toolbar, form, list, and dialogs.
    def reload() -> None:
        refresh("Tickets reloaded from the database.")

    def change_filter(event: ft.Event[ft.Dropdown]) -> None:
        try:
            selected = validate_filter(event.control.value or FILTER_ALL)
        except ValueError as error:
            feedback(str(error), ok=False)
            return
        refresh(status_filter=selected)

    def create_ticket(title: str, priority: int) -> str | None:
        try:
            new_id = register.create_ticket(title, priority)
        except (sqlite3.Error, TypeError, ValueError, RuntimeError) as error:
            return f"Could not save ticket: {error}"
        refresh(f"Ticket {new_id} saved.")
        return None

    def toggle_ticket_status(ticket: Ticket) -> None:
        try:
            updated = register.toggle_ticket_status(ticket["id"])
        except (sqlite3.Error, ValueError) as error:
            feedback(f"Could not update ticket status: {error}", ok=False)
            return
        message = (
            f"Ticket {ticket['id']} status updated."
            if updated
            else f"Ticket {ticket['id']} has already been deleted."
        )
        refresh(message, ok=updated)

    def request_delete(ticket: Ticket) -> None:
        nonlocal delete_ticket
        delete_ticket = ticket
        set_delete_ticket(ticket)

    def confirm_delete() -> None:
        ticket = delete_ticket
        if ticket is None:
            return
        close_delete_dialog()
        try:
            deleted = register.delete_ticket(ticket["id"])
        except (sqlite3.Error, ValueError) as error:
            feedback(f"Could not delete ticket: {error}", ok=False)
            return
        message = (
            f"Ticket {ticket['id']} deleted."
            if deleted
            else f"Ticket {ticket['id']} has already been deleted."
        )
        refresh(message, ok=deleted)

    def open_ticket(ticket: Ticket) -> None:
        nonlocal detail_ticket
        detail_ticket = ticket
        set_detail_ticket(ticket)

    def toggle_from_details() -> None:
        ticket = detail_ticket
        if ticket is None:
            return
        close_detail_dialog()
        toggle_ticket_status(ticket)

    def delete_from_details() -> None:
        ticket = detail_ticket
        if ticket is None:
            return
        close_detail_dialog()
        request_delete(ticket)

    tickets = tickets_state["tickets"]
    current_filter = tickets_state["status_filter"]
    error = tickets_state["error"]
    return ft.Container(
        padding=PAGE_PADDING,
        expand=True,
        content=ft.Stack(
            fit=ft.StackFit.EXPAND,
            controls=[
                ft.Column(
                    scroll=ft.ScrollMode.AUTO,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    spacing=16,
                    controls=[
                        AppHeader(),
                        TicketForm(on_create=create_ticket, on_feedback=feedback),
                        ft.Divider(),
                        TicketToolbar(
                            status_filter=current_filter,
                            on_reload=reload,
                            on_filter=change_filter,
                        ),
                        ft.Text(
                            "*Click the status icon to toggle a ticket between "
                            "Open and Completed.",
                            key="ticket-status-hint",
                            italic=True,
                            size=14,
                            color=ft.Colors.BLUE_GREY_700,
                        ),
                        ft.Text(
                            f"{len(tickets)} tickets · Filter: {current_filter}",
                            key="ticket-count",
                        ),
                        ft.Text(
                            error or "",
                            color=ft.Colors.ERROR,
                            visible=error is not None,
                        ),
                        TicketList(
                            tickets=tickets,
                            on_open=open_ticket,
                            status_filter=current_filter,
                            on_delete=request_delete,
                            on_toggle_status=toggle_ticket_status,
                        ),
                    ],
                ),
                TicketDetailDialog(
                    ticket=detail_ticket,
                    on_toggle=toggle_from_details,
                    on_delete=delete_from_details,
                    on_close=close_detail_dialog,
                ),
                DeleteTicketDialog(
                    ticket=delete_ticket,
                    on_confirm=confirm_delete,
                    on_cancel=close_delete_dialog,
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

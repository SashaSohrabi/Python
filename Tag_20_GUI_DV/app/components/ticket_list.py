# pyright: strict
from collections.abc import Callable, Sequence

import flet as ft

from ..constants.ticket_status import FILTER_ALL, STATUS_COMPLETED
from ..types.ticket_types import Ticket, TicketFilter
from .ticket_status_icon import build_ticket_status_icon


def build_ticket_card(
    ticket: Ticket,
    on_open: Callable[[Ticket], None],
    on_delete: Callable[[Ticket], None],
    on_toggle_status: Callable[[Ticket], None],
) -> ft.Container:
    def open_ticket() -> None:
        on_open(ticket)

    def request_delete() -> None:
        on_delete(ticket)

    def request_status_toggle() -> None:
        on_toggle_status(ticket)

    return ft.Container(
        key=f"ticket-{ticket['id']}",
        bgcolor=(
            ft.Colors.GREEN_100
            if ticket["status"] == STATUS_COMPLETED
            else ft.Colors.AMBER_100
        ),
        border_radius=8,
        margin=2,
        content=ft.ListTile(
            leading=build_ticket_status_icon(
                ticket["status"],
                request_status_toggle,
                key=f"toggle-ticket-status-{ticket['id']}",
            ),
            title=ft.Text(
                f"#{ticket['id']} · {ticket['title']}",
                color=ft.Colors.BLUE_GREY_900,
                weight=ft.FontWeight.W_600,
            ),
            subtitle=ft.Text(
                f"Priority {ticket['priority']} · Status: {ticket['status']}",
                color=ft.Colors.BLUE_GREY_800,
                size=12,
            ),
            trailing=ft.IconButton(
                key=f"delete-ticket-{ticket['id']}",
                icon=ft.Icons.DELETE_OUTLINE,
                icon_color=ft.Colors.ERROR,
                tooltip=f"Delete ticket {ticket['id']}",
                on_click=request_delete,
            ),
            on_click=open_ticket,
        ),
    )


@ft.component
def TicketList(
    tickets: Sequence[Ticket],
    on_open: Callable[[Ticket], None],
    status_filter: TicketFilter,
    on_delete: Callable[[Ticket], None],
    on_toggle_status: Callable[[Ticket], None],
) -> ft.Column:
    if not tickets:
        message = (
            "No tickets yet. Create one using the form above."
            if status_filter == FILTER_ALL
            else f"No {status_filter} tickets match this filter."
        )
        return ft.Column(controls=[ft.Text(message, key="empty-ticket-list")])
    return ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        spacing=6,
        controls=[
            build_ticket_card(ticket, on_open, on_delete, on_toggle_status)
            for ticket in tickets
        ],
    )

# pyright: strict
from collections.abc import Callable
from functools import partial

import flet as ft

from ..constants.constants import STATUS_COMPLETED
from ..types.types import Ticket
from .ticket_status_icon import TicketStatusIcon


@ft.component
def TicketItem(
    ticket: Ticket,
    on_open: Callable[[Ticket], None],
    on_delete: Callable[[Ticket], None],
    on_toggle_status: Callable[[Ticket], None],
    *,
    key: str | None = None,
) -> ft.Container:
    return ft.Container(
        key=key or f"ticket-{ticket['id']}",
        bgcolor=(
            ft.Colors.GREEN_100
            if ticket["status"] == STATUS_COMPLETED
            else ft.Colors.AMBER_100
        ),
        border_radius=8,
        margin=2,
        content=ft.ListTile(
            leading=TicketStatusIcon(
                status=ticket["status"],
                on_toggle=partial(on_toggle_status, ticket),
                button_key=f"toggle-ticket-status-{ticket['id']}",
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
                on_click=partial(on_delete, ticket),
            ),
            on_click=partial(on_open, ticket),
        ),
    )

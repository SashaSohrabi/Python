# pyright: strict
from collections.abc import Callable

import flet as ft

from ..types.types import Ticket


@ft.component
def TicketDetailDialog(
    ticket: Ticket | None,
    on_toggle: Callable[[], None],
    on_delete: Callable[[], None],
    on_close: Callable[[], None],
) -> ft.AlertDialog:
    return ft.AlertDialog(
        open=ticket is not None,
        modal=False,
        title=ft.Text(ticket["title"] if ticket else ""),
        content=ft.Text(
            f"Ticket {ticket['id']} · Priority {ticket['priority']} · "
            f"Status: {ticket['status']}"
            if ticket
            else ""
        ),
        actions=[
            ft.TextButton("Switch status", on_click=on_toggle),
            ft.TextButton("Delete…", on_click=on_delete),
            ft.TextButton("Close", on_click=on_close),
        ],
        on_dismiss=on_close,
    )

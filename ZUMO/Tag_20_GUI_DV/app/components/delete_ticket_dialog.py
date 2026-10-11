# pyright: strict
from collections.abc import Callable

import flet as ft

from ..types.types import Ticket


@ft.component
def DeleteTicketDialog(
    ticket: Ticket | None,
    on_confirm: Callable[[], None],
    on_cancel: Callable[[], None],
) -> ft.AlertDialog:
    return ft.AlertDialog(
        open=ticket is not None,
        modal=True,
        title=ft.Text(f"Delete ticket {ticket['id']}?" if ticket else "Delete ticket?"),
        content=ft.Column(
            tight=True,
            spacing=12,
            controls=[
                ft.Text(ticket["title"] if ticket else "", weight=ft.FontWeight.W_600),
                ft.Text("This permanently removes the ticket from the database."),
            ],
        ),
        actions=[
            ft.TextButton("Cancel", on_click=on_cancel),
            ft.TextButton(
                "Yes, delete",
                style=ft.ButtonStyle(color=ft.Colors.ERROR),
                on_click=on_confirm,
            ),
        ],
        on_dismiss=on_cancel,
    )

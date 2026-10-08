# pyright: strict
from collections.abc import Callable

import flet as ft

from ..types.ticket_types import Ticket


def build_detail_dialog(
    ticket: Ticket,
    on_toggle: Callable[[], None],
    on_delete: Callable[[], None],
    on_close: Callable[[], None],
    error_text: ft.Text,
) -> ft.AlertDialog:
    return ft.AlertDialog(
        modal=True,
        title=ft.Text(ticket["title"]),
        content=ft.Column(
            tight=True,
            controls=[
                ft.Text(
                    f"Ticket {ticket['id']} · Priority {ticket['priority']} · "
                    f"Status: {ticket['status']}"
                ),
                error_text,
            ],
        ),
        actions=[
            ft.TextButton("Switch status", on_click=on_toggle),
            ft.TextButton("Delete…", on_click=on_delete),
            ft.TextButton("Close", on_click=on_close),
        ],
    )

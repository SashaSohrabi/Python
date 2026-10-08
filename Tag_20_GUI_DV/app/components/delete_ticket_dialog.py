# pyright: strict
from collections.abc import Callable

import flet as ft

from ..types.state_types import DeleteTicketState


def build_delete_dialog(
    state: DeleteTicketState,
    on_confirm: Callable[[], None],
    on_cancel: Callable[[], None],
    error_text: ft.Text | None = None,
) -> ft.AlertDialog | None:
    ticket = state["ticket"]
    if ticket is None:
        return None
    return ft.AlertDialog(
        modal=True,
        title=ft.Text(f"Delete ticket {ticket['id']}?"),
        content=ft.Column(
            tight=True,
            spacing=12,
            controls=[
                ft.Text(ticket["title"], weight=ft.FontWeight.W_600),
                ft.Text("This permanently removes the ticket from the database."),
                (
                    error_text
                    if error_text is not None
                    else ft.Text(
                        state["error"] or "",
                        color=ft.Colors.ERROR,
                        visible=state["error"] is not None,
                    )
                ),
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
    )

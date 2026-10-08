# pyright: strict
from collections.abc import Callable

import flet as ft

from ..constants.ticket_status import STATUS_COMPLETED
from ..types.ticket_types import TicketStatus


def build_ticket_status_icon(
    status: TicketStatus,
    on_toggle: Callable[[], None],
    *,
    key: str,
) -> ft.Container:
    completed = status == STATUS_COMPLETED
    label = status.capitalize()
    action = "reopen ticket" if completed else "mark as completed"
    return ft.Container(
        width=40,
        height=40,
        alignment=ft.Alignment.CENTER,
        border_radius=12,
        bgcolor=ft.Colors.GREEN_50 if completed else ft.Colors.AMBER_50,
        content=ft.IconButton(
            key=key,
            width=40,
            height=40,
            padding=0,
            tooltip=f"{label}: {action}",
            on_click=on_toggle,
            icon=ft.Icon(
                ft.Icons.CHECK_CIRCLE if completed else ft.Icons.PENDING_ACTIONS,
                size=26,
                color=ft.Colors.GREEN_800 if completed else ft.Colors.AMBER_900,
                semantics_label=label,
            ),
        ),
    )

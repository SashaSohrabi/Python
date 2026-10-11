# pyright: strict
from collections.abc import Callable

import flet as ft

from ..constants.constants import FILTER_ALL, STATUS_COMPLETED, STATUS_OPEN
from ..types.types import TicketFilter


@ft.component
def TicketToolbar(
    status_filter: TicketFilter,
    on_reload: Callable[[], None],
    on_filter: Callable[[ft.Event[ft.Dropdown]], None],
) -> ft.Row:
    return ft.Row(
        wrap=True,
        controls=[
            ft.Button("Reload", icon=ft.Icons.REFRESH, on_click=on_reload),
            ft.Dropdown(
                key="ticket-filter",
                label="Status",
                width=180,
                value=status_filter,
                options=[
                    ft.DropdownOption(FILTER_ALL, text="All"),
                    ft.DropdownOption(STATUS_OPEN, text="Open"),
                    ft.DropdownOption(STATUS_COMPLETED, text="Completed"),
                ],
                on_select=on_filter,
            ),
        ],
    )

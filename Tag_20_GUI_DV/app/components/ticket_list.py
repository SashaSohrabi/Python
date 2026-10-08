# pyright: strict
from collections.abc import Callable, Sequence

import flet as ft

from ..constants.constants import FILTER_ALL
from ..types.types import Ticket, TicketFilter
from .ticket_item import TicketItem


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
            TicketItem(
                ticket=ticket,
                on_open=on_open,
                on_delete=on_delete,
                on_toggle_status=on_toggle_status,
                key=f"ticket-{ticket['id']}",
            )
            for ticket in tickets
        ],
    )

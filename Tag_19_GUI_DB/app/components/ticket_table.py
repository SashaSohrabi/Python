# pyright: strict
"""Aligned ticket columns with a delete action at the right of each row."""

from collections.abc import Callable, Sequence
from typing import Final

import flet as ft

from ..types.ticket_types import Ticket
from .ticket_status_icon import build_ticket_status_icon

PRIORITY_COLUMN_WIDTH: Final[int] = 72
STATUS_COLUMN_WIDTH: Final[int] = 64
ACTIONS_COLUMN_WIDTH: Final[int] = 64


def centered_column_content(content: ft.Control, width: int) -> ft.Container:
    return ft.Container(width=width, alignment=ft.Alignment.CENTER, content=content)


def build_ticket_row(
    ticket: Ticket,
    on_delete: Callable[[Ticket], None],
    on_toggle_status: Callable[[Ticket], None],
) -> ft.DataRow:

    def request_delete() -> None:
        on_delete(ticket)

    def request_status_toggle() -> None:
        on_toggle_status(ticket)

    return ft.DataRow(
        key=str(ticket["id"]),
        cells=[
            ft.DataCell(ft.Text(str(ticket["id"]))),
            ft.DataCell(
                ft.Text(
                    ticket["title"],
                    width=300,
                    max_lines=3,
                    overflow=ft.TextOverflow.ELLIPSIS,
                    tooltip=ticket["title"],
                )
            ),
            ft.DataCell(
                centered_column_content(
                    ft.Text(str(ticket["priority"])), PRIORITY_COLUMN_WIDTH
                )
            ),
            ft.DataCell(
                centered_column_content(
                    build_ticket_status_icon(
                        ticket["status"],
                        request_status_toggle,
                        key=f"toggle-ticket-status-{ticket['id']}",
                    ),
                    STATUS_COLUMN_WIDTH,
                )
            ),
            ft.DataCell(
                centered_column_content(
                    ft.IconButton(
                        key=f"delete-ticket-{ticket['id']}",
                        icon=ft.Icons.DELETE_OUTLINE,
                        icon_color=ft.Colors.ERROR,
                        tooltip=f"Delete ticket {ticket['id']}",
                        on_click=request_delete,
                    ),
                    ACTIONS_COLUMN_WIDTH,
                )
            ),
        ],
    )


@ft.component
def TicketTable(
    tickets: Sequence[Ticket],
    on_delete: Callable[[Ticket], None],
    on_toggle_status: Callable[[Ticket], None],
) -> ft.Column:
    return ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    ft.DataTable(
                        columns=[
                            ft.DataColumn(label=ft.Text("ID"), numeric=True),
                            ft.DataColumn(label=ft.Text("Title")),
                            ft.DataColumn(
                                label=centered_column_content(
                                    ft.Text("Priority"), PRIORITY_COLUMN_WIDTH
                                ),
                                heading_row_alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            ft.DataColumn(
                                label=centered_column_content(
                                    ft.Text("Status"), STATUS_COLUMN_WIDTH
                                ),
                                heading_row_alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            ft.DataColumn(
                                label=centered_column_content(
                                    ft.Text("Actions"), ACTIONS_COLUMN_WIDTH
                                ),
                                heading_row_alignment=ft.MainAxisAlignment.CENTER,
                            ),
                        ],
                        rows=[
                            build_ticket_row(ticket, on_delete, on_toggle_status)
                            for ticket in tickets
                        ],
                        column_spacing=20,
                        horizontal_margin=12,
                        data_row_min_height=64,
                        data_row_max_height=90,
                        heading_row_color=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                        show_bottom_border=True,
                    ),
                ],
            ),
            ft.Text("No tickets found.", visible=not tickets),
        ],
    )

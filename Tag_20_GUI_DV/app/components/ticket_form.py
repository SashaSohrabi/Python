# pyright: strict
from collections.abc import Callable

import flet as ft

from ..models.validation import parse_priority, validate_title
from ..state import State
from ..types.flet_types import use_state


@ft.component
def TicketForm(
    on_create: Callable[[str, int], str | None],
    state: State,
    on_feedback: Callable[[str, bool], None],
) -> ft.Column:
    form, set_form = use_state(state.create_ticket_form_state)

    def change_title(event: ft.Event[ft.TextField]) -> None:
        value = event.control.value or ""
        set_form(
            lambda previous: {
                **previous,
                "title": value,
                "title_error": None,
                "save_error": None,
            }
        )

    def change_priority(event: ft.Event[ft.Dropdown]) -> None:
        value = event.control.value or ""
        set_form(
            lambda previous: {
                **previous,
                "priority": value,
                "priority_error": None,
                "save_error": None,
            }
        )

    def submit_ticket() -> None:
        title_error: str | None = None
        priority_error: str | None = None
        title = ""
        priority = 0
        try:
            title = validate_title(form["title"])
        except ValueError as error:
            title_error = str(error)

        try:
            priority = parse_priority(form["priority"])
        except ValueError as error:
            priority_error = str(error)

        if title_error is not None or priority_error is not None:
            set_form(
                {
                    **form,
                    "title_error": title_error,
                    "priority_error": priority_error,
                    "save_error": None,
                }
            )
            on_feedback(
                title_error or priority_error or "Please check the form.", False
            )
            return
        save_error = on_create(title, priority)

        if save_error is not None:
            set_form({**form, "save_error": save_error})
            on_feedback(save_error, False)
            return
        # Clear the title only after a successful commit; preserve the priority.
        set_form(state.create_ticket_form_state(priority=form["priority"]))

    return ft.Column(
        spacing=12,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        controls=[
            ft.Text("New ticket", size=20, weight=ft.FontWeight.W_600),
            ft.ResponsiveRow(
                controls=[
                    ft.TextField(
                        key="ticket-title",
                        label="Title",
                        hint_text="e.g. Printer on the 3rd floor is jammed",
                        value=form["title"],
                        error=form["title_error"],
                        col={"xs": 12, "sm": 9},
                        on_change=change_title,
                        on_submit=submit_ticket,
                    ),
                    ft.Dropdown(
                        key="ticket-priority",
                        label="Priority",
                        value=form["priority"],
                        error_text=form["priority_error"],
                        col={"xs": 12, "sm": 3},
                        options=[ft.DropdownOption(str(value)) for value in (1, 2, 3)],
                        on_select=change_priority,
                    ),
                ],
            ),
            ft.Text(
                form["save_error"] or "",
                color=ft.Colors.ERROR,
                visible=form["save_error"] is not None,
            ),
            ft.Button("Create ticket", icon=ft.Icons.ADD, on_click=submit_ticket),
        ],
    )

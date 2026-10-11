# pyright: strict
from collections.abc import Callable

import flet as ft

from ..services.validation import parse_priority, validate_title
from ..types.types import StateSetter, TicketFormState, use_state


def empty_form(priority: str = "2") -> TicketFormState:
    return {
        "title": "",
        "priority": priority,
        "title_error": None,
        "priority_error": None,
        "save_error": None,
    }


def form_handlers(
    form: TicketFormState,
    set_form: StateSetter[TicketFormState],
    on_create: Callable[[str, int], str | None],
    on_feedback: Callable[[str, bool], None],
) -> tuple[
    Callable[[ft.Event[ft.TextField]], None],
    Callable[[ft.Event[ft.Dropdown]], None],
    Callable[[], None],
]:
    def change_title(event: ft.Event[ft.TextField]) -> None:
        nonlocal form
        value = event.control.value or ""
        form = {**form, "title": value, "title_error": None, "save_error": None}
        set_form(form)

    def change_priority(event: ft.Event[ft.Dropdown]) -> None:
        nonlocal form
        value = event.control.value or ""
        form = {**form, "priority": value, "priority_error": None, "save_error": None}
        set_form(form)

    def submit_ticket() -> None:
        nonlocal form
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
            form = {
                **form,
                "title_error": title_error,
                "priority_error": priority_error,
                "save_error": None,
            }
            set_form(form)
            on_feedback(
                title_error or priority_error or "Please check the form.", False
            )
            return
        save_error = on_create(title, priority)

        if save_error is not None:
            form = {**form, "save_error": save_error}
            set_form(form)
            on_feedback(save_error, False)
            return
        # Clear the title only after a successful commit; preserve the priority.
        form = empty_form(priority=form["priority"])
        set_form(form)

    return change_title, change_priority, submit_ticket


@ft.component
def TicketForm(
    on_create: Callable[[str, int], str | None],
    on_feedback: Callable[[str, bool], None],
) -> ft.Column:
    form, set_form = use_state(empty_form)
    change_title, change_priority, submit_ticket = form_handlers(
        form, set_form, on_create, on_feedback
    )

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

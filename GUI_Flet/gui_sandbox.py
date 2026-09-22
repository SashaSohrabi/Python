import flet as ft


@ft.component
def counter() -> ft.Row:
    count, set_count = ft.use_state(0)

    def minus_click(_e: ft.Event[ft.IconButton]) -> None:
        set_count(count - 1)

    def plus_click(_e: ft.Event[ft.IconButton]) -> None:
        set_count(count + 1)

    def input_change(_e: ft.Event[ft.TextField]) -> None:
        try:
            number = int(_e.control.value or "0")
        except ValueError:
            _e.control.value = str(count)
            _e.control.update()
            return
        set_count(number)

    return ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.IconButton(ft.Icons.REMOVE, on_click=minus_click),
            ft.TextField(
                value=str(count),
                input_filter=ft.InputFilter(
                    allow=True,
                    regex_string=r"^[0-9]*$",
                ),
                text_align=ft.TextAlign.RIGHT,
                width=100,
                on_change=input_change,
            ),
            ft.IconButton(ft.Icons.ADD, on_click=plus_click),
        ],
    )


def main(page: ft.Page) -> None:
    page.title = "Flet counter example"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.render(counter)


ft.run(main)

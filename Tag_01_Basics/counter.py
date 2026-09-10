import flet as ft


def main(page: ft.Page) -> None:
    page.title = "Flet counter example"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    input = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

    def minus_click(e: ft.Event[ft.IconButton]) -> None:
        input.value = str(int(input.value or "0") - 1)

    def plus_click(e: ft.Event[ft.IconButton]) -> None:
        input.value = str(int(input.value or "0") + 1)

    page.add(
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.IconButton(ft.Icons.REMOVE, on_click=minus_click),
                input,
                ft.IconButton(ft.Icons.ADD, on_click=plus_click),
            ],
        )
    )


# Flet 0.86.5 leaves run()'s deprecated target parameter untyped.
ft.run(main)  # pyright: ignore[reportUnknownMemberType]

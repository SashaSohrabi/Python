# pyright: strict
import flet as ft

from ..constants.constants import APP_SUBTITLE, APP_TITLE


@ft.component
def AppHeader() -> ft.Container:
    return ft.Container(
        bgcolor=ft.Colors.INDIGO_500,
        padding=20,
        border_radius=8,
        content=ft.Column(
            spacing=4,
            controls=[
                ft.Text(
                    APP_TITLE,
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),
                ft.Text(APP_SUBTITLE, color=ft.Colors.WHITE),
            ],
        ),
    )

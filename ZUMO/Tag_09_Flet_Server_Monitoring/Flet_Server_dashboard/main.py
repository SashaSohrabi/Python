"""
Skript: Server Dashboard
Autor: Sasha Sohrabi
Datum: 22.09.2026
Zweck: Dashboard mit drei Karten und der Warn-Statuszeil
"""

import flet as ft
from app.views.dashboard import server_dashboard


def main(page: ft.Page) -> None:
    page.title = "Server-Dashboard"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO
    page.appbar = ft.AppBar(
        title=ft.Text("Server-Dashboard")
    )

    page.render(server_dashboard)


if __name__ == "__main__":
    ft.run(main)

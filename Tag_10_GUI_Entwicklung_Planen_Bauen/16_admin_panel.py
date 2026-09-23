# Skriptname: 16_admin_panel.py
# Autor: Sasha Sohrabi
# Datum: 23.09.2026
# Zweck: Fenster konfigurieren und das modulare Admin-Panel starten.

import flet as ft
from app.constants import settings, theme
from app.views.admin_panel import admin_panel


def main(page: ft.Page) -> None:
    """Konfiguriert das Fenster; die Ansicht setzt die Module zusammen."""
    page.title = settings.APP_TITEL
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed=theme.TEXTFARBE)
    page.bgcolor = theme.HINTERGRUND
    page.padding = settings.SEITENABSTAND
    page.scroll = ft.ScrollMode.AUTO
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.window.width = settings.FENSTER_BREITE
    page.window.height = settings.FENSTER_HOEHE
    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.Icons.ADMIN_PANEL_SETTINGS_OUTLINED, color=ft.Colors.WHITE),
        title=ft.Text(settings.APP_TITEL, weight=ft.FontWeight.BOLD),
        bgcolor=theme.TEXTFARBE,
        color=ft.Colors.WHITE,
        toolbar_height=settings.APPBAR_HOEHE,
    )
    page.add(admin_panel())


if __name__ == "__main__":
    ft.run(main)

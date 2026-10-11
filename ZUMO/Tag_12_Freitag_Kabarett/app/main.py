# Skriptname: main.py
# Autor: Sasha Sohrabi
# Datum: 25.09.2026
# Zweck: Das Server-Kabarett-Fenster konfigurieren und mit Objekten füllen.

import flet as ft
from app.constants import settings, theme
from app.data.infrastructure import serverliste_erzeugen
from app.views.dashboard import kabarett_dashboard


def main(page: ft.Page) -> None:
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
        leading=ft.Icon(ft.Icons.MIC_ROUNDED, color=ft.Colors.WHITE),
        title=ft.Text(settings.APP_TITEL, weight=ft.FontWeight.BOLD),
        bgcolor=theme.TEXTFARBE,
        color=ft.Colors.WHITE,
        toolbar_height=settings.APPBAR_HOEHE,
    )

    truppe = serverliste_erzeugen()
    page.add(kabarett_dashboard(truppe))

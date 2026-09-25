# Skriptname: server_card.py
# Autor: Sasha Sohrabi
# Datum: 25.09.2026
# Zweck: Alle Serverklassen mit derselben Kartenfunktion darstellen.

import flet as ft
from app.constants import theme
from app.models.server import Server


def server_karte(server: Server) -> ft.Container:
    if server.status == "offline":
        farbe = theme.FEHLER
        icon = ft.Icons.ERROR_OUTLINE
    elif server.ist_kritisch():
        farbe = theme.WARNUNG
        icon = ft.Icons.WARNING_AMBER_OUTLINED
    else:
        farbe = theme.ERFOLG
        icon = ft.Icons.CHECK_CIRCLE_OUTLINE

    return ft.Container(
        bgcolor=theme.KARTENFARBE,
        border=ft.Border(left=ft.BorderSide(4, farbe)),
        border_radius=8,
        padding=16,
        content=ft.Column(
            spacing=8,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(icon, color=farbe, size=24),
                        ft.Text(
                            str(server),
                            size=17,
                            weight=ft.FontWeight.BOLD,
                            color=theme.TEXTFARBE,
                            expand=True,
                        ),
                    ],
                ),
                ft.Text(server.diagnose(), color=farbe, size=14),
            ],
        ),
    )

# Skriptname: server_card.py
# Autor: Sasha Sohrabi
# Datum: 28.09.2026
# Zweck: Alle Servertypen über dieselbe polymorphe Kartenfunktion darstellen.

import flet as ft

from ..constants import theme
from ..models.server import Server


def server_karte(server: Server) -> ft.Container:
    if server.ist_offline():
        farbe, icon = theme.FEHLER, ft.Icons.CLOUD_OFF
        zustand = "Offline"
    elif server.ist_kritisch():
        farbe, icon = theme.WARNUNG, ft.Icons.WARNING_AMBER_OUTLINED
        zustand = "Kritisch"
    else:
        farbe, icon = theme.ERFOLG, ft.Icons.CHECK_CIRCLE_OUTLINE
        zustand = "Stabil"

    typ = type(server).__name__
    typ_text = "Server · Basisklasse" if type(server) is Server else f"{typ} ← Server"

    return ft.Container(
        bgcolor=theme.KARTENFARBE,
        border=ft.Border(left=ft.BorderSide(4, farbe)),
        border_radius=8,
        padding=14,
        content=ft.Column(
            spacing=6,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(icon, color=farbe, size=24),
                        ft.Text(
                            str(server), size=16, weight=ft.FontWeight.BOLD,
                            color=theme.TEXTFARBE, expand=True,
                        ),
                    ],
                ),
                ft.Text(
                    f"{typ_text} · IP {server.ip} · {zustand}",
                    color=theme.NEBENTEXT, size=12,
                ),
                ft.Text(server.diagnose(), color=farbe, size=14),
            ],
        ),
    )

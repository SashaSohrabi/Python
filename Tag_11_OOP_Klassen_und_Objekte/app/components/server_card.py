# Skriptname: server_card.py
# Autor: Sasha Sohrabi
# Datum: 24.09.2026
# Zweck: Einen Server anhand seiner Attribute und Methode als Ampelkarte anzeigen.

import flet as ft
from app.constants import theme
from app.models.server import Server


def server_karte(server: Server) -> ft.Container:
    if server.status == "offline":
        farbe = theme.FEHLER
        meldung = "Offline – Server nicht verfügbar."
        icon = ft.Icons.ERROR_OUTLINE
    elif server.ist_kritisch():
        farbe = theme.WARNUNG
        meldung = f"Kritisch – CPU-Last bei {server.cpu_load} %."
        icon = ft.Icons.WARNING_AMBER_OUTLINED
    else:
        farbe = theme.ERFOLG
        meldung = f"Online – CPU-Last bei {server.cpu_load} %."
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
                            server.name,
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=theme.TEXTFARBE,
                            expand=True,
                        ),
                    ],
                ),
                ft.Text(
                    f"{server.ip} · {server.rolle} · CPU {server.cpu_load} %",
                    color=theme.NEBENTEXT,
                    size=14,
                ),
                ft.Text(meldung, color=farbe, size=14),
            ],
        ),
    )

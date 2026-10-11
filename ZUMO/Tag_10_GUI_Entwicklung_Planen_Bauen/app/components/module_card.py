# Skriptname: module_card.py
# Autor: Sasha Sohrabi
# Datum: 23.09.2026
# Zweck: Einheitliches Kartenlayout für die Admin-Werkzeuge.

import flet as ft
from app.constants.theme import AKZENT, KARTENFARBE, NEBENTEXT, TEXTFARBE


def modul_karte(
    titel: str, icon: ft.IconData, beschreibung: str, controls: list[ft.Control]
) -> ft.Container:
    """Verbindet Titel, Beschreibung und Inhalt zu einer Modulkarte."""
    return ft.Container(
        bgcolor=KARTENFARBE,
        border=ft.Border(left=ft.BorderSide(4, AKZENT)),
        border_radius=8,
        padding=16,
        content=ft.Column(
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(icon, color=TEXTFARBE, size=22),
                        ft.Text(titel, size=19, weight=ft.FontWeight.BOLD, expand=True),
                    ]
                ),
                ft.Text(beschreibung, size=13, color=NEBENTEXT),
                *controls,
            ],
        ),
    )

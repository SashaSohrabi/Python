# Skriptname: show_card.py
# Autor: Sasha Sohrabi
# Datum: 25.09.2026
# Zweck: Ein Auftritt als visuelle Karte mit Status und Publikum anzeigen.

import flet as ft
from app.constants import theme
from app.models.show import Show


def show_karte(auftritt: Show) -> ft.Container:
    if auftritt.status == "pause":
        farbe = theme.FEHLER
        meldung = "Pause – noch keine Live-Phase."
        icon = ft.Icons.PAUSE_CIRCLE_OUTLINE
    elif auftritt.ist_highlight():
        farbe = theme.WARNUNG
        meldung = f"Highlight – Publikum {auftritt.publikum}% begeistert."
        icon = ft.Icons.STAR_OUTLINE
    else:
        farbe = theme.ERFOLG
        meldung = f"Stabil – Publikum {auftritt.publikum}% zufrieden."
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
                            auftritt.name,
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=theme.TEXTFARBE,
                            expand=True,
                        ),
                    ],
                ),
                ft.Text(
                    f"{auftritt.kuenstler} · {auftritt.genre} · {auftritt.dauer_min} min",
                    color=theme.NEBENTEXT,
                    size=13,
                ),
                ft.Text(meldung, color=farbe, size=13),
            ],
        ),
    )

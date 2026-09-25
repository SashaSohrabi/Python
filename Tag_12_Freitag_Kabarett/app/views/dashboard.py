# Skriptname: dashboard.py
# Autor: Sasha Sohrabi
# Datum: 25.09.2026
# Zweck: Auftrittskarten zusammenfassen und Highlights bewerten.

import flet as ft
from app.components.show_card import show_karte
from app.constants import theme
from app.constants.settings import KARTENABSTAND
from app.models.show import Show


def kabarett_dashboard(auffuehrungen: list[Show]) -> ft.Column:
    karten = ft.Column(
        controls=[show_karte(auftritt) for auftritt in auffuehrungen],
        spacing=KARTENABSTAND,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
    )
    ergebnis = ft.Text(
        "Noch keine Bewertung durchgeführt.", color=theme.NEBENTEXT, size=14
    )

    def pruefen() -> None:
        highlights = [auftritt for auftritt in auffuehrungen if auftritt.ist_highlight()]
        karten.controls = [show_karte(auftritt) for auftritt in auffuehrungen]

        if not auffuehrungen:
            ergebnis.value = "Keine Auftritte im Programm vorhanden."
            ergebnis.color = theme.FEHLER
        elif highlights:
            namen = ", ".join(auftritt.name for auftritt in highlights)
            ergebnis.value = (
                f"Highlight-Check: {len(highlights)} Auftritte mit starkem Publikum: "
                f"{namen}."
            )
            ergebnis.color = theme.WARNUNG
        else:
            ergebnis.value = "Kein klarer Publikumshighlight gefunden."
            ergebnis.color = theme.ERFOLG

    return ft.Column(
        spacing=KARTENABSTAND,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        controls=[
            ft.Text(
                "PROGRAMM / FREITAG KABARETT",
                color=theme.NEBENTEXT,
                size=12,
            ),
            ft.Text(
                "Live = aktiv · Pause = ausgesetzt · Highlight = Publikum stärker als 80 %",
                color=theme.NEBENTEXT,
                size=13,
            ),
            karten,
            ft.Row(
                wrap=True,
                controls=[
                    ft.Button(
                        "Highlights prüfen",
                        icon=ft.Icons.STAR_OUTLINE,
                        on_click=pruefen,
                    ),
                ],
            ),
            ergebnis,
            ft.Text(
                "Die Bewertung fokussiert auf starke Reaktionen im Publikum und hebt die besten Nummern hervor.",
                color=theme.NEBENTEXT,
                size=12,
            ),
        ],
    )

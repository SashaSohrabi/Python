# Skriptname: dashboard.py
# Autor: Sasha Sohrabi
# Datum: 24.09.2026
# Zweck: Serverkarten zusammenstellen und CPU-kritische Objekte auf Knopfdruck prüfen.

import flet as ft
from app.components.server_card import server_karte
from app.constants import theme
from app.constants.settings import CPU_WARNGRENZE, KARTENABSTAND
from app.models.server import Server


def server_dashboard(serverliste: list[Server]) -> ft.Column:
    karten = ft.Column(
        controls=[server_karte(server) for server in serverliste],
        spacing=KARTENABSTAND,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
    )
    ergebnis = ft.Text(
        "Noch keine Prüfung durchgeführt.", color=theme.NEBENTEXT, size=14
    )

    def pruefen() -> None:
        kritisch = [server for server in serverliste if server.ist_kritisch()]
        karten.controls = [server_karte(server) for server in serverliste]
        if not serverliste:
            ergebnis.value = "Keine Server zur Prüfung vorhanden."
            ergebnis.color = theme.FEHLER
        elif kritisch:
            namen = ", ".join(server.name for server in kritisch)
            ergebnis.value = (
                f"CPU-Warnung: {len(kritisch)} von {len(serverliste)} Servern kritisch: "
                f"{namen}."
            )
            ergebnis.color = theme.WARNUNG
        else:
            ergebnis.value = "Keine CPU-kritischen Server gefunden."
            ergebnis.color = theme.ERFOLG
        

    return ft.Column(
        spacing=KARTENABSTAND,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        controls=[
            ft.Text("SERVERÜBERSICHT / LOKALE BEISPIELDATEN", color=theme.NEBENTEXT, size=12),
            ft.Text(
                f"Grün: online · Gelb: online und CPU über {CPU_WARNGRENZE} % · Rot: offline",
                color=theme.NEBENTEXT,
                size=13,
            ),
            karten,
            ft.Row(
                wrap=True,
                controls=[
                    ft.Button(
                        "Kritische Server prüfen",
                        icon=ft.Icons.FACT_CHECK_OUTLINED,
                        on_click=pruefen,
                    ),
                ],
            ),
            ergebnis,
            ft.Text(
                "Die Prüfung zählt Online-Server mit hoher CPU-Last. "
                "Offline-Server bleiben als rotes Problem in den Karten sichtbar.",
                color=theme.NEBENTEXT,
                size=12,
            ),
        ],
    )

# Skriptname: analyzer.py
# Autor: Sasha Sohrabi
# Datum: 23.09.2026
# Zweck: Hostnamen im Inventar suchen und Serverinformationen anzeigen.

import flet as ft
from app.components.feedback import rueckmeldung
from app.components.module_card import modul_karte
from app.constants.theme import NEBENTEXT
from app.services.analyzer import server_suchen
from app.services.monitoring import server_status
from app.state import STATE


def modul_analyzer() -> ft.Container:
    """Verbindet die Hostnameneingabe mit Suche und Statusanzeige."""
    hostname = ft.TextField(
        label="Hostname",
        hint_text="z. B. web-01, db-01 oder backup-01",
        dense=True,
        expand=True,
        autocorrect=False,
    )
    ergebnis = ft.Text("Noch kein Server gesucht.", color=NEBENTEXT, size=13)

    def analysieren() -> None:
        try:
            name, daten = server_suchen(hostname.value, STATE.infrastructure)
        except ValueError as exc:
            hostname.error = str(exc)
            rueckmeldung(ergebnis, "Suche fehlgeschlagen. Bitte die Eingabe prüfen.", "fehler")
            ergebnis.update()
            return
        hostname.error = None
        status_text, status = server_status(daten)
        rueckmeldung(
            ergebnis,
            f"Gefunden: {name} · {daten['rolle']} · IP {daten['ip']} · {status_text}",
            status,
        )

    hostname.on_submit = analysieren
    return modul_karte(
        "02  Hostname-Analyzer",
        ft.Icons.SEARCH,
        "Rolle, IP-Adresse und Status aus dem lokalen Server-Inventar abrufen.",
        [
            ft.ResponsiveRow(
                controls=[
                    ft.Container(hostname, col={"xs": 12, "sm": 8}),
                    ft.Container(
                        ft.Button("Server suchen", icon=ft.Icons.SEARCH, on_click=analysieren),
                        col={"xs": 12, "sm": 4},
                    ),
                ],
            ),
            ergebnis,
        ],
    )

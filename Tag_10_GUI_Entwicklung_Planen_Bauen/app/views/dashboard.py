# Skriptname: dashboard.py
# Autor: Sasha Sohrabi
# Datum: 23.09.2026
# Zweck: Serverzustände darstellen und das Demo-Inventar auswerten.

from datetime import datetime

import flet as ft
from app.components.feedback import rueckmeldung
from app.components.module_card import modul_karte
from app.constants.settings import CPU_WARNGRENZE
from app.constants.theme import STATUSFARBEN
from app.data.infrastructure import refresh_infrastruktur
from app.services.monitoring import server_status
from app.state import STATE


def modul_dashboard() -> ft.Container:
    """Zeigt die Server und wertet ihre Zustände auf Knopfdruck aus."""
    server_liste = ft.Column(spacing=4)
    ergebnis = ft.Text(size=13)

    def aktualisieren() -> None:
        STATE.infrastructure = refresh_infrastruktur()
        infrastruktur = STATE.infrastructure
        server_liste.controls.clear()
        auffaellig = 0
        for name, daten in infrastruktur.items():
            status_text, status = server_status(daten)
            auffaellig += status != "ok"
            server_liste.controls.append(
                ft.Row(
                    wrap=True,
                    spacing=8,
                    run_spacing=2,
                    controls=[
                        ft.Text(name, weight=ft.FontWeight.BOLD, width=110),
                        ft.Text(f"{daten['ip']} · {daten['rolle']}", size=13),
                        ft.Text(status_text, color=STATUSFARBEN[status], size=13),
                    ],
                )
            )
        zeit = datetime.now().strftime("%H:%M:%S")
        if not infrastruktur:
            rueckmeldung(ergebnis, "Kein Server im Inventar hinterlegt.", "fehler")
        elif auffaellig:
            rueckmeldung(
                ergebnis,
                f"{auffaellig} von {len(infrastruktur)} Servern benötigen Aufmerksamkeit. "
                f"Ausgewertet um {zeit}.",
                "fehler",
            )
        else:
            rueckmeldung(ergebnis, f"Alle Server unauffällig. Ausgewertet um {zeit}.", "ok")

    aktualisieren()
    return modul_karte(
        "01  Server-Dashboard",
        ft.Icons.DNS_OUTLINED,
        f"Lokale Beispieldaten · CPU über {CPU_WARNGRENZE} % = Warnung · Offline = Problem",
        [
            server_liste,
            ergebnis,
            ft.Row(
                controls=[
                    ft.Button(
                        "Status aktualisieren", icon=ft.Icons.REFRESH, on_click=aktualisieren
                    )
                ]
            ),
        ],
    )

# Skriptname: dashboard.py
# Autor: Sasha Sohrabi
# Datum: 28.09.2026
# Zweck: Vier Serverkarten und eine typweise gruppierte Prüfung anzeigen.

import flet as ft

from ..components.server_card import server_karte
from ..constants import settings, theme
from ..models.server import Server
from ..services.monitoring import statusbericht


def server_dashboard(serverliste: list[Server]) -> ft.Column:
    statuszeile = ft.Text(
        "Noch nicht geprüft. Starte die Prüfung über den Button.",
        color=theme.NEBENTEXT, size=14,
    )

    def kritische_server_pruefen() -> None:
        statuszeile.value = statusbericht(serverliste)
        statuszeile.color = theme.TEXTFARBE
        # Flet 1.0 aktualisiert nach dem Event-Handler automatisch.

    return ft.Column(
        spacing=settings.KARTENABSTAND,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        controls=[
            ft.Text("VIER SYSTEME. DREI SERVERTYPEN.", color=theme.NEBENTEXT, size=12),
            ft.Text(
                f"CPU-Regeln: Server > {settings.CPU_WARNGRENZE} % · "
                f"Backup > {settings.BACKUP_WARNGRENZE} % oder offline · "
                f"Legacy ab {settings.LEGACY_WARNGRENZE} % (online)",
                color=theme.NEBENTEXT, size=13,
            ),
            ft.Text(
                "Grün: stabil · Gelb: kritisch und online · Rot: offline",
                color=theme.NEBENTEXT, size=13,
            ),
            ft.Column(
                controls=[server_karte(server) for server in serverliste],
                spacing=settings.KARTENABSTAND,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            ),
            ft.Container(
                bgcolor=theme.KARTENFARBE,
                border_radius=8,
                padding=16,
                content=ft.Column(
                    spacing=10,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    controls=[
                        ft.Text(
                            "Infrastruktur prüfen", size=18,
                            weight=ft.FontWeight.BOLD, color=theme.TEXTFARBE,
                        ),
                        ft.Row(
                            wrap=True,
                            controls=[
                                ft.Button(
                                    "Kritische Server prüfen",
                                    icon=ft.Icons.FACT_CHECK_OUTLINED,
                                    on_click=kritische_server_pruefen,
                                ),
                            ],
                        ),
                        statuszeile,
                    ],
                ),
            ),
        ],
    )

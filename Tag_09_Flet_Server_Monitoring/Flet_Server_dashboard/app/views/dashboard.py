from collections.abc import Callable
from typing import cast

import flet as ft
from app.components.server_card import server_karte
from app.data.infrastructure import get_infrastruktur
from app.models.server import DatenbankServer
from app.services.monitoring import monitoring_status
from flet import use_state  # pyright: ignore[reportUnknownVariableType]

# Flet 1.0 lässt den Updater-Typ offen; hier werden Wert und Setter präzisiert.
type State[T] = tuple[T, Callable[[T | Callable[[T], T]], None]]


@ft.component
def server_dashboard() -> ft.Column:
    infrastruktur, set_infrastruktur = cast(
        State[dict[str, DatenbankServer]], use_state(get_infrastruktur())
    )

    def status_neu_laden(_e: ft.Event[ft.Button]) -> None:
        set_infrastruktur(get_infrastruktur())

    meldung, hat_warnung = monitoring_status(infrastruktur)

    farbe = (
        ft.Colors.RED
        if hat_warnung
        else ft.Colors.GREEN
    )

    return ft.Column(
        controls=[
            ft.Text(
                meldung,
                size=16,
                weight=ft.FontWeight.BOLD,
                color=farbe,
            ),
            ft.Column(
                controls=[
                    server_karte(name, daten)
                    for name, daten in infrastruktur.items()
                ],
                spacing=12,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            ),
            ft.Button(
                content="Status neu laden",
                on_click=status_neu_laden,
            ),
        ],
        spacing=12,
    )

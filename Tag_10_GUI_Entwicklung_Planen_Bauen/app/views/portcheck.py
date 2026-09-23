# Skriptname: portcheck.py
# Autor: Sasha Sohrabi
# Datum: 23.09.2026
# Zweck: Portnummern entgegennehmen und ihre lokale Freigabe anzeigen.

import flet as ft
from app.components.module_card import modul_karte
from app.constants.theme import NEBENTEXT, STATUSFARBEN
from app.data.ports import get_freigegebene_ports, refresh_freigegebene_ports
from app.services.portcheck import port_pruefen
from app.state import STATE


def modul_portcheck() -> ft.Container:
    """Verbindet die Eingabe mit der Prüfung gegen die sichtbare Freigabeliste."""
    if not STATE.freigaben:
        STATE.freigaben = get_freigegebene_ports()

    port = ft.TextField(
        label="Portnummer",
        hint_text="Ganze Zahl von 1 bis 65535, z. B. 443",
        dense=True,
        keyboard_type=ft.KeyboardType.NUMBER,
        expand=True,
    )
    ergebnis = ft.Text(value=STATE.port_result, color=STATE.port_color, size=13)
    freigaben_text = ft.Text(
        "Freigaben: "
        + " · ".join(
            f"{nummer} {dienst}" for nummer, dienst in sorted(STATE.freigaben.items())
        ),
        color=NEBENTEXT,
        size=12,
    )

    def pruefen() -> None:
        # Jeder Klick erzeugt genau die neue Liste, die angezeigt und geprüft wird.
        freigaben = refresh_freigegebene_ports()
        STATE.freigaben = freigaben
        freigaben_text.value = "Freigaben: " + " · ".join(
            f"{nummer} {dienst}" for nummer, dienst in sorted(freigaben.items())
        )
        try:
            nummer, dienst = port_pruefen(port.value, freigaben)
        except ValueError as exc:
            port.error = str(exc)
            STATE.port_result = str(exc)
            STATE.port_color = STATUSFARBEN["fehler"]
        else:
            port.error = None
            if dienst is None:
                STATE.port_result = (
                    f"Port {nummer} ist nicht in der Freigabeliste "
                    "und damit nicht verfügbar."
                )
                STATE.port_color = STATUSFARBEN["fehler"]
            else:
                STATE.port_result = (
                    f"Port {nummer} ({dienst}) ist in der Freigabeliste "
                    "und damit verfügbar."
                )
                STATE.port_color = STATUSFARBEN["ok"]

        ergebnis.value = STATE.port_result
        ergebnis.color = STATE.port_color
        karte.update()

    port.on_submit = pruefen
    karte = modul_karte(
        "03  Port-Freigabecheck",
        ft.Icons.SECURITY,
        "Jeder Klick erzeugt eine neue zufällige Freigabeliste und prüft die Eingabe dagegen.",
        [
            ft.ResponsiveRow(
                controls=[
                    ft.Container(port, col={"xs": 12, "sm": 8}),
                    ft.Container(
                        ft.Button(
                            "Port prüfen",
                            icon=ft.Icons.FACT_CHECK_OUTLINED,
                            on_click=pruefen,
                        ),
                        col={"xs": 12, "sm": 4},
                    ),
                ],
            ),
            ergebnis,
            freigaben_text,
        ],
    )

    return karte
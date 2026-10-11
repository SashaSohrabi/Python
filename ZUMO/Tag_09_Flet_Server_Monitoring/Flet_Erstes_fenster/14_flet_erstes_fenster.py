# Skriptname: 14_flet_erstes_fenster.py
# Autor: Sasha Sohrabi
# Datum: 22.09.2026
# Zweck: Ein erstes Flet-Fenster mit Hostname-Eingabe und farbiger Rückmeldung.

from collections.abc import Callable
from typing import cast

import flet as ft
from flet import use_state  # pyright: ignore[reportUnknownVariableType]

# Flet 1.0 typisiert den Updater nicht vollständig; der Setter darf auch
# eine Funktion annehmen, die aus dem bisherigen Wert den nächsten berechnet.
type State[T] = tuple[T, Callable[[T | Callable[[T], T]], None]]


@ft.component
def server_toolbox() -> ft.Column:
    hostname, set_hostname = cast(State[str], use_state(""))
    # str und Colors erlauben alle Texte/Farben, nicht nur die Startwerte.
    output, set_output = cast(
        State[tuple[str, ft.Colors]], use_state(("", ft.Colors.BLACK))
    )

    def hostname_aendern(e: ft.Event[ft.TextField]) -> None:
        set_hostname(e.control.value or "")

    def analysieren(_e: ft.Event[ft.Button]) -> None:
        name = hostname.strip()

        if not name:
            set_output(("Bitte einen Hostnamen eingeben!", ft.Colors.RED))
        else:
            set_output((f"Server '{name}' wird analysiert.", ft.Colors.GREEN))

    return ft.Column(
        spacing=16,
        controls=[
            ft.Text(
                "Willkommen in der Server-Toolbox!",
                size=24,
                weight=ft.FontWeight.BOLD,
            ),
            ft.TextField(
                label="Hostname",
                hint_text="z. B. web-01",
                value=hostname,
                width=420,
                on_change=hostname_aendern,
            ),
            ft.Button(content="Analysieren", on_click=analysieren),
            ft.Text(value=output[0], color=output[1], size=16),
        ],
    )


def main(page: ft.Page) -> None:
    page.title = "Server-Toolbox"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 24
    page.spacing = 16
    page.scroll = ft.ScrollMode.AUTO
    page.render(server_toolbox)


if __name__ == "__main__":
    ft.run(main)

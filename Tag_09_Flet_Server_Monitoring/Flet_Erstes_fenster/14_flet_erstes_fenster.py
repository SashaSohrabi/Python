# Skriptname: 14_flet_erstes_fenster.py
# Autor: Sasha Sohrabi
# Datum: 22.09.2026
# Zweck: Ein erstes Flet-Fenster mit Hostname-Eingabe und farbiger Rückmeldung.

import flet as ft


@ft.component
def server_toolbox() -> ft.Column:
    hostname, set_hostname = ft.use_state("")
    initial_output: tuple[str, ft.Colors] = ("", ft.Colors.BLACK)
    output, set_output = ft.use_state(initial_output)

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

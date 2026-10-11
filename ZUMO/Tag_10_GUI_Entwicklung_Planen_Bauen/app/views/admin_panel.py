# Skriptname: admin_panel.py
# Autor: Sasha Sohrabi
# Datum: 23.09.2026
# Zweck: Die vier unabhängigen Admin-Werkzeuge in einer Ansicht zusammenstellen.

import flet as ft
from app.constants.settings import MODULABSTAND
from app.constants.theme import NEBENTEXT
from app.views.analyzer import modul_analyzer
from app.views.dashboard import modul_dashboard
from app.views.notes import modul_notizen
from app.views.portcheck import modul_portcheck


def admin_panel() -> ft.Column:
    """Baut die gemeinsame Oberfläche aus den eigenständigen Modulansichten."""
    return ft.Column(
        spacing=MODULABSTAND,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        controls=[
            ft.Text(
                "SYSTEMADMINISTRATION / LOKALES DEMO-INVENTAR", color=NEBENTEXT, size=12
            ),
            modul_dashboard(),
            modul_analyzer(),
            modul_portcheck(),
            modul_notizen(),
        ],
    )

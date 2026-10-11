# Skriptname: dashboard.py
# Autor: Sasha Sohrabi
# Datum: 25.09.2026
# Zweck: Fünf polymorphe Serverkarten und ein Diagnose-Orakel zusammenstellen.

import random

import flet as ft
from app.components.server_card import server_karte
from app.constants import theme
from app.constants.settings import CPU_WARNGRENZE, KARTENABSTAND
from app.data.diagnoses import DIAGNOSEN
from app.models.server import Server


def kabarett_dashboard(truppe: list[Server]) -> ft.Column:
    orakel_text = ft.Text(
        "Das Orakel wartet auf seinen ersten Kaffee. Klicke auf den Button.",
        color=theme.NEBENTEXT,
        size=14,
    )

    def diagnose_wuerfeln() -> None:
        orakel_text.value = random.choice(DIAGNOSEN)
        orakel_text.color = theme.TEXTFARBE

    return ft.Column(
        spacing=KARTENABSTAND,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        controls=[
            ft.Text("FÜNF SERVER. EINE BÜHNE.", color=theme.NEBENTEXT, size=12),
            ft.Text(
                f"Grün: online · Gelb: online und CPU über {CPU_WARNGRENZE} % · Rot: offline",
                color=theme.NEBENTEXT,
                size=13,
            ),
            ft.Column(
                controls=[server_karte(server) for server in truppe],
                spacing=KARTENABSTAND,
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
                            "Diagnose-Orakel",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=theme.TEXTFARBE,
                        ),
                        orakel_text,
                        ft.Row(
                            wrap=True,
                            controls=[
                                ft.Button(
                                    "Diagnose würfeln",
                                    icon=ft.Icons.CASINO_OUTLINED,
                                    on_click=diagnose_wuerfeln,
                                ),
                            ],
                        ),
                    ],
                ),
            ),
        ],
    )

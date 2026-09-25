import flet as ft
from app.models.server import DatenbankServer


def server_karte(name: str, daten: DatenbankServer) -> ft.Container:
    farbe = (
        ft.Colors.GREEN_100
        if daten["status"] == "online"
        else ft.Colors.RED_100
    )

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(name, size=20, weight=ft.FontWeight.BOLD),
                ft.Text(f"IP-Adresse: {daten['ip']}"),
                ft.Text(f"Rolle: {daten['rolle']}"),
                ft.Text(f"CPU-Last: {daten['cpu_load']} %"),
                ft.Text(f"Status: {daten['status']}"),
            ],
            spacing=4,
        ),
        bgcolor=farbe,
        padding=12,
        border_radius=8,
    )
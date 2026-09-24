# Skriptname: infrastructure.py
# Autor: Sasha Sohrabi
# Datum: 24.09.2026
# Zweck: Die drei Beispielserver des Arbeitsauftrags als neue Objekte erzeugen.

from app.models.server import Server


def serverliste_erzeugen() -> list[Server]:
    return [
        Server("web-01", "192.168.1.10", "Frontend", 45, "online"),
        Server("db-01", "192.168.1.20", "Datenbank", 92, "online"),
        Server("backup-01", "192.168.1.30", "Backup", 5, "offline"),
    ]

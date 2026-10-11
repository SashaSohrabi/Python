# Skriptname: infrastructure.py
# Autor: Sasha Sohrabi
# Datum: 25.09.2026
# Zweck: Die gemischte Server-Truppe des Arbeitsauftrags erzeugen.

from app.models.server import BackupServer, DruckerServer, LegacyServer, Server


def serverliste_erzeugen() -> list[Server]:
    return [
        Server("web-01", "Frontend", 45, "online"),
        Server("db-01", "Datenbank", 92, "online"),
        BackupServer("backup-01", "192.168.1.30", 3, "online", "2014"),
        DruckerServer("printer-01", "Etage 2", 12, "online"),
        LegacyServer("legacy-01", "Keller", 8, "online"),
    ]

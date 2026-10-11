# Skriptname: infrastructure.py
# Autor: Sasha Sohrabi
# Datum: 23.09.2026
# Zweck: Ein zentrales Server-Inventar, das für Dashboard und Suche konsistent bleibt.

import random
from copy import deepcopy
from typing import Final

from app.models.server import Server

_SERVER_ROLES: Final[dict[str, str]] = {
    "web-01": "Frontend",
    "db-01": "Datenbank",
    "backup-01": "Backup",
}

_current_infrastruktur: dict[str, Server] = {}


def _generate_infrastruktur() -> dict[str, Server]:
    """Erzeugt eine neue, zufällige Infrastruktur-Struktur."""
    infrastruktur: dict[str, Server] = {}
    for name, rolle in _SERVER_ROLES.items():
        infrastruktur[name] = {
            "ip": f"192.168.1.{random.randint(10, 99)}",
            "rolle": rolle,
            "cpu_load": random.randint(0, 100),
            "status": random.choice(["online", "offline"]),
        }
    return infrastruktur


def refresh_infrastruktur() -> dict[str, Server]:
    """Erzeugt eine neue aktuelle Infrastruktur-Snapshot und überschreibt den aktuellen Stand."""
    global _current_infrastruktur
    _current_infrastruktur = _generate_infrastruktur()
    return deepcopy(_current_infrastruktur)


def get_infrastruktur() -> dict[str, Server]:
    """Gibt den aktuellen, konsistenten Snapshot zurück."""
    if not _current_infrastruktur:
        refresh_infrastruktur()
    return deepcopy(_current_infrastruktur)

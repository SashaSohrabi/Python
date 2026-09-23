# Skriptname: ports.py
# Autor: Sasha Sohrabi
# Datum: 23.09.2026
# Zweck: Ein zentraler Freigabe-Snapshot für Anzeige und Portprüfung.

import random
from copy import deepcopy
from typing import Final

_PORT_DIENSTE: Final[dict[int, str]] = {
    22: "SSH",
    53: "DNS",
    80: "HTTP",
    443: "HTTPS",
    3306: "MySQL",
    5432: "PostgreSQL",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
}

_current_freigegebene_ports: dict[int, str] = {}


def _generate_freigegebene_ports() -> dict[int, str]:
    """Erzeugt eine neue, zufällige Auswahl freigegebener Ports."""
    anzahl = random.randint(3, 5)
    return dict(random.sample(sorted(_PORT_DIENSTE.items()), k=anzahl))


def refresh_freigegebene_ports() -> dict[int, str]:
    """Erzeugt einen neuen aktuellen Port-Snapshot und überschreibt den vorhandenen Stand."""
    global _current_freigegebene_ports
    _current_freigegebene_ports = _generate_freigegebene_ports()
    return deepcopy(_current_freigegebene_ports)


def get_freigegebene_ports() -> dict[int, str]:
    """Gibt den aktuell gültigen Port-Snapshot zurück."""
    if not _current_freigegebene_ports:
        refresh_freigegebene_ports()
    return deepcopy(_current_freigegebene_ports)

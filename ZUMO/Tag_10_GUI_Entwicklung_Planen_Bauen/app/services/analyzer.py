# Skriptname: analyzer.py
# Autor: Sasha Sohrabi
# Datum: 23.09.2026
# Zweck: Hostnamen prüfen und Datensätze im Server-Inventar finden.

import re

from app.constants.settings import MAX_HOSTNAME_LAENGE
from app.models.server import Server


def server_suchen(
    eingabe: str, infrastruktur: dict[str, Server]
) -> tuple[str, Server]:
    """Validiert einen einfachen Hostnamen und sucht ihn in den lokalen Daten."""
    name = eingabe.strip()
    if not name:
        raise ValueError("Bitte einen Hostnamen eingeben.")
    if len(name) > MAX_HOSTNAME_LAENGE:
        raise ValueError(
            f"Ein Hostname darf höchstens {MAX_HOSTNAME_LAENGE} Zeichen enthalten."
        )
    if not name.isascii() or re.fullmatch(
        r"[a-z0-9](?:[a-z0-9-]*[a-z0-9])?", name.lower()
    ) is None:
        raise ValueError(
            "Nur Buchstaben A–Z, Ziffern und Bindestriche sind erlaubt; "
            "am Anfang und Ende darf kein Bindestrich stehen."
        )
    name = name.lower()
    if name not in infrastruktur:
        raise ValueError(f"Server '{name}' ist nicht in der Infrastruktur hinterlegt.")
    return name, infrastruktur[name]

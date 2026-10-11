# Skriptname: monitoring.py
# Autor: Sasha Sohrabi
# Datum: 23.09.2026
# Zweck: Serverstatus anhand von Erreichbarkeitsmerkmal und CPU-Last bewerten.

from app.constants.settings import CPU_WARNGRENZE
from app.models.server import Server
from app.models.status import Status


def server_status(server: Server) -> tuple[str, Status]:
    """Offline hat Vorrang vor der CPU-Warnung."""
    if server["status"] == "offline":
        return "Offline – Server nicht verfügbar.", "fehler"
    if server["cpu_load"] > CPU_WARNGRENZE:
        return f"Warnung – CPU-Last bei {server['cpu_load']} %.", "warnung"
    return f"Online – CPU-Last bei {server['cpu_load']} %.", "ok"

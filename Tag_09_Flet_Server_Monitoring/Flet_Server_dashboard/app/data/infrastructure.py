from copy import deepcopy

from app.models.server import DatenbankServer


_INFRASTRUKTUR: dict[str, DatenbankServer] = {
    "web-01": {
        "ip": "192.168.1.10",
        "rolle": "Frontend",
        "cpu_load": 45,
        "status": "online",
    },
    "db-01": {
        "ip": "192.168.1.20",
        "rolle": "Datenbank",
        "cpu_load": 92,
        "status": "online",
    },
    "backup-01": {
        "ip": "192.168.1.30",
        "rolle": "Backup",
        "cpu_load": 0,
        "status": "offline",
    },
}


def get_infrastruktur() -> dict[str, DatenbankServer]:
    return deepcopy(_INFRASTRUKTUR)
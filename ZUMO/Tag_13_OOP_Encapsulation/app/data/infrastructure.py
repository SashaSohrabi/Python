# Skriptname: infrastructure.py
# Autor: Sasha Sohrabi
# Datum: 28.09.2026
# Zweck: Vier Systeme mit drei unterschiedlichen Servertypen erzeugen.

from ..models.server import BackupServer, LegacyServer, Server
from ..types.server_status import ServerStatusEnum


def infrastruktur_erzeugen() -> list[Server]:
    return [
        Server("web-01", "192.168.1.10", "Frontend", 45, ServerStatusEnum.ONLINE),
        BackupServer(
            "backup-01", "192.168.1.30", 5, ServerStatusEnum.OFFLINE, "24.09. 03:00"
        ),
        LegacyServer(
            "alt-vm-1", "192.168.1.99", 71, ServerStatusEnum.ONLINE, "2023-11"
        ),
        Server("db-01", "192.168.1.20", "Datenbank", 92, ServerStatusEnum.ONLINE),
    ]

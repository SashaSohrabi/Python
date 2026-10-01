# pyright: strict
"""Sample servers in the order used by the assignment."""

from ..models.backup_server import BackupServer
from ..models.server import Server
from ..models.web_server import WebServer
from ..types.server_status import ServerStatusEnum


def sample_servers() -> list[Server]:
    return [
        Server("web-01", "192.168.1.10", "Frontend", 45, ServerStatusEnum.ONLINE),
        WebServer("web-02", "10.0.0.12", 55, ServerStatusEnum.ONLINE, "beta"),
        BackupServer("backup-01", "192.168.1.30", 5, ServerStatusEnum.OFFLINE, "2014"),
        Server("db-01", "192.168.1.20", "Database", 92, ServerStatusEnum.ONLINE),
    ]

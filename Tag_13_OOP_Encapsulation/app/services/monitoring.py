# Skriptname: monitoring.py
# Autor: Sasha Sohrabi
# Datum: 28.09.2026
# Zweck: Kritische Server per isinstance gruppieren und einen Status zurückgeben.

from ..models.server import BackupServer, LegacyServer, Server


def kritische_server_gruppieren(serverliste: list[Server]) -> dict[str, list[str]]:
    gruppen: dict[str, list[str]] = {
        "Server": [],
        "BackupServer": [],
        "LegacyServer": [],
    }
    for server in serverliste:
        if not server.ist_kritisch():
            continue
        if isinstance(server, BackupServer):
            gruppen["BackupServer"].append(server.name)
        elif isinstance(server, LegacyServer):
            gruppen["LegacyServer"].append(server.name)
        else:
            gruppen["Server"].append(server.name)
    return gruppen


def statusbericht(serverliste: list[Server]) -> str:
    gruppen = kritische_server_gruppieren(serverliste)
    anzahl = sum(len(namen) for namen in gruppen.values())
    details = " | ".join(
        f"{typ}: {', '.join(namen) if namen else 'keine'}"
        for typ, namen in gruppen.items()
    )
    return f"Kritische Server: {anzahl}\n{details}"

# Skriptname: 18a_wiederholung.py
# Autor: Sasha Sohrabi
# Datum: 29.09.2026
# Zweck: WebServer und ReverseProxyServer samt Vererbung und Kapselung vorführen.

import argparse

from app.models.server import (
    BackupServer,
    LegacyServer,
    ReverseProxyServer,
    Server,
    WebServer,
)
from app.types.server_status import ServerStatusEnum


def ist_instanz(objekt: object, klasse: type[object]) -> bool:
    return isinstance(objekt, klasse)


def wiederholung() -> None:
    web = WebServer("web-01", "10.0.0.11", 45, ServerStatusEnum.ONLINE, "nginx")
    beta = WebServer("web-02", "10.0.0.12", 55, ServerStatusEnum.ONLINE, "beta")
    db = Server("db-01", "10.0.0.20", "Datenbank", 92, ServerStatusEnum.ONLINE)
    liste: list[Server] = [web, beta, db]

    print("=== Aufgabe 2: WebServer ===")
    for server in liste:
        print(server)
    print(f"isinstance(web, WebServer): {ist_instanz(web, WebServer)}")
    print(f"isinstance(web, Server): {ist_instanz(web, Server)}")

    try:
        db.cpu_load = 180
    except ValueError as fehler:
        print(f"db.cpu_load = 180 -> ValueError: {fehler}")
    print(f"db.cpu_load bleibt: {db.cpu_load}")

    try:
        web.framework = "traefik"  # type: ignore
    except AttributeError as fehler:
        print(f"web.framework = 'traefik' -> AttributeError: {fehler}")
    print(f"web.framework bleibt: {web.framework}")

    print("\n=== Aufgabe 2b: ReverseProxyServer ===")
    proxy = ReverseProxyServer(
        "proxy-01", "10.0.0.5", 30, ServerStatusEnum.ONLINE, "nginx", 2
    )
    print(proxy)
    print(
        f"isinstance(proxy, ReverseProxyServer): {ist_instanz(proxy, ReverseProxyServer)}"
    )
    print(f"isinstance(proxy, WebServer): {ist_instanz(proxy, WebServer)}")
    print(f"isinstance(proxy, Server): {ist_instanz(proxy, Server)}")
    print(f"proxy.ist_kritisch(): {proxy.ist_kritisch()}")
    try:
        proxy.backend_count = 99  # type: ignore
    except AttributeError as fehler:
        print(f"proxy.backend_count = 99 -> AttributeError: {fehler}")
    print(f"proxy.backend_count bleibt: {proxy.backend_count}")
    print(
        "super().__init__() ruft hier WebServer.__init__() auf, weil Python "
        "in der Methodenauflösungsreihenfolge nach ReverseProxyServer "
        "mit WebServer fortfährt."
    )

    ohne_backends = ReverseProxyServer(
        "proxy-02", "10.0.0.6", 30, ServerStatusEnum.ONLINE, "nginx", 0
    )
    print(f"Proxy ohne Backends: kritisch = {ohne_backends.ist_kritisch()}")

    print()
    print("\n=== Aufgabe 3: Ausgabe und Zustandsänderung ===")
    for server in liste:
        print(server.name, "→", server.ist_kritisch())
    print(ist_instanz(liste[0], Server))
    print(ist_instanz(liste[2], WebServer))
    liste[0].cpu_load = 71
    print(liste[0].ist_kritisch())
    print(f"web-01 nach cpu_load = 71: kritisch = {web.ist_kritisch()}")


def auswertung() -> None:
    print("=== Auswertung: Server, BackupServer, LegacyServer ===")
    backup = BackupServer(
        "backup-01", "192.168.1.30", 5, ServerStatusEnum.OFFLINE, "24.09. 03:00"
    )
    serverliste: list[Server] = [
        Server("web-01", "192.168.1.10", "Frontend", 45, ServerStatusEnum.ONLINE),
        backup,
        LegacyServer(
            "alt-vm-1", "192.168.1.99", 71, ServerStatusEnum.ONLINE, "2023-11"
        ),
        Server("db-01", "192.168.1.20", "Datenbank", 92, ServerStatusEnum.ONLINE),
    ]
    for server in serverliste:
        print(server)
        print(f"  ist_kritisch(): {server.ist_kritisch()}")

    print(f"isinstance(backup, BackupServer): {ist_instanz(backup, BackupServer)}")
    print(f"isinstance(backup, Server): {ist_instanz(backup, Server)}")
    print(
        f"isinstance(serverliste[0], BackupServer): {ist_instanz(serverliste[0], BackupServer)}"
    )
    print(f"type(backup) is Server: {type(backup) is Server}")
    for wert in (180, 88, "x"):
        try:
            serverliste[0].cpu_load = wert  # type: ignore
        except (ValueError, TypeError) as fehler:
            print(f"cpu_load = {wert!r} -> {type(fehler).__name__}: {fehler}")
        else:
            print(f"cpu_load = {wert!r} -> akzeptiert")

    print("\n=== Name-Mangling: Umbenennung, keine Zugriffssperre ===")

    class StrengPrivat:
        def __init__(self) -> None:
            self.__geheim = 42

    objekt = StrengPrivat()
    try:
        print(getattr(objekt, "__geheim"))
    except AttributeError as fehler:
        print(f"objekt.__geheim -> AttributeError: {fehler}")
    print(f"objekt._StrengPrivat__geheim -> {getattr(objekt, '_StrengPrivat__geheim')}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Aufgabe 18a: Wiederholung OOP II")
    parser.add_argument(
        "--auswertung",
        action="store_true",
        help="Zusätzlich die Beispiele aus Auswertung_OOP_II.pdf ausführen",
    )
    args = parser.parse_args()
    wiederholung()
    if args.auswertung:
        print()
        auswertung()

# Skriptname: server.py
# Autor: Sasha Sohrabi
# Datum: 23.09.2026
# Zweck: Gemeinsames Datenschema eines Servers.

from typing import Literal, TypedDict


class Server(TypedDict):
    """Ein Serverdatensatz aus der Beispiel-Infrastruktur."""

    ip: str
    rolle: str
    cpu_load: int
    status: Literal["online", "offline"]

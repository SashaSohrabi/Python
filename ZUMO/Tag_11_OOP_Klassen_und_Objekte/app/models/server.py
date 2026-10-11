# Skriptname: server.py
# Autor: Sasha Sohrabi
# Datum: 24.09.2026
# Zweck: Serverdaten und die zugehörige CPU-Prüfung in einer Klasse bündeln.

from typing import Literal

from app.constants.settings import CPU_WARNGRENZE


class Server:
    def __init__(
        self,
        name: str,
        ip: str,
        rolle: str,
        cpu_load: int,
        status: Literal["online", "offline"],
    ) -> None:
        self.name = name
        self.ip = ip
        self.rolle = rolle
        self.cpu_load = cpu_load
        self.status = status

    def ist_kritisch(self) -> bool:
        return self.status == "online" and self.cpu_load > CPU_WARNGRENZE

    def __str__(self) -> str:
        zustand = "läuft" if self.status == "online" else "offline"
        return f"{self.name} ({self.rolle}) – CPU {self.cpu_load} % – {zustand}"

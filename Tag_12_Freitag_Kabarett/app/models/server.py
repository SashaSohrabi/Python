# Skriptname: server.py
# Autor: Sasha Sohrabi
# Datum: 25.09.2026
# Zweck: Server als Basisklasse und drei Kabarett-Subklassen modellieren.

from typing import Literal

from app.constants.settings import CPU_WARNGRENZE


class Server:
    def __init__(
        self,
        name: str,
        rolle: str,
        cpu_load: int,
        status: Literal["online", "offline"],
    ) -> None:
        self.name = name
        self.rolle = rolle
        self.cpu_load = cpu_load
        self.status = status

    def ist_kritisch(self) -> bool:
        return self.status == "online" and self.cpu_load > CPU_WARNGRENZE

    def diagnose(self) -> str:
        if self.status == "offline":
            return f"{self.name}: Offline – Server nicht verfügbar."
        if self.ist_kritisch():
            return f"{self.name}: Warnung – CPU-Last bei {self.cpu_load} %."
        return f"{self.name}: Online – läuft stabil bei {self.cpu_load} % CPU-Last."

    def __str__(self) -> str:
        zustand = "läuft" if self.status == "online" else "offline"
        return f"{self.name} ({self.rolle}) – CPU {self.cpu_load} % – {zustand}"


class BackupServer(Server):
    def __init__(
        self,
        name: str,
        ip: str,
        cpu_load: int,
        status: Literal["online", "offline"],
        laufzeit_seit: str,
    ) -> None:
        super().__init__(name, "Backup", cpu_load, status)
        self.ip = ip
        self.laufzeit_seit = laufzeit_seit

    def diagnose(self) -> str:
        return f"{self.name}: Das Backup läuft. Schon seit {self.laufzeit_seit}."


class DruckerServer(Server):
    def diagnose(self) -> str:
        return (
            f"{self.name}: Druckauftrag angenommen. Wird irgendwann kommen. Vielleicht."
        )


class LegacyServer(Server):
    def diagnose(self) -> str:
        return f"{self.name}: In meinen Zeiten hat man Server noch zu Fuß aktualisiert."

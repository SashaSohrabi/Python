# Skriptname: server.py
# Autor: Sasha Sohrabi
# Datum: 28.09.2026
# Zweck: Serverdaten kapseln und kritische Zustände polymorph bestimmen.

from typing import Literal

from ..constants.settings import (
    BACKUP_WARNGRENZE,
    CPU_WARNGRENZE,
    LEGACY_WARNGRENZE,
)
from ..types.server_status import ServerStatusEnum

ServerStatus = Literal[
    ServerStatusEnum.ONLINE,
    ServerStatusEnum.OFFLINE,
]


class Server:
    def __init__(
        self,
        name: str,
        ip: str,
        rolle: str,
        cpu_load: int,
        status: ServerStatusEnum,
    ) -> None:
        self._name = name
        self._ip = ip
        self._rolle = rolle
        self.cpu_load = cpu_load
        self.status = status

    @property
    def name(self) -> str:
        return self._name

    @property
    def ip(self) -> str:
        return self._ip

    @property
    def rolle(self) -> str:
        return self._rolle

    @property
    def cpu_load(self) -> int:
        return self._cpu_load

    @cpu_load.setter
    def cpu_load(self, wert: int) -> None:
        if type(wert) is not int:
            raise TypeError("cpu_load muss eine ganze Zahl (int) sein")
        if not 0 <= wert <= 100:
            raise ValueError("cpu_load muss zwischen 0 und 100 liegen")
        self._cpu_load = wert

    @property
    def status(self) -> ServerStatusEnum:
        return self._status

    @status.setter
    def status(self, wert: ServerStatusEnum) -> None:
        try:
            self._status = ServerStatusEnum(wert)
        except ValueError as exc:
            raise ValueError("status muss 'online' oder 'offline' sein") from exc

    def ist_offline(self) -> bool:
        return self.status == ServerStatusEnum.OFFLINE

    def ist_kritisch(self) -> bool:
        return not self.ist_offline() and self.cpu_load > CPU_WARNGRENZE

    def diagnose(self) -> str:
        if self.ist_offline():
            return f"{self.name}: Offline - Server nicht verfügbar."
        if self.ist_kritisch():
            return f"{self.name}: Warnung - CPU-Last bei {self.cpu_load} %."
        return f"{self.name}: Online - läuft stabil bei {self.cpu_load} % CPU-Last."

    def __str__(self) -> str:
        return (
            f"{self.name} ({self.rolle}) - CPU {self.cpu_load} % - {self.status.value}"
        )


class BackupServer(Server):
    def __init__(
        self,
        name: str,
        ip: str,
        cpu_load: int,
        status: ServerStatusEnum,
        letzte_sicherung: str,
    ) -> None:
        super().__init__(name, ip, "Backup", cpu_load, status)
        self._letzte_sicherung = letzte_sicherung

    @property
    def letzte_sicherung(self) -> str:
        return self._letzte_sicherung

    def ist_kritisch(self) -> bool:
        return self.ist_offline() or self.cpu_load > BACKUP_WARNGRENZE

    def __str__(self) -> str:
        return f"{super().__str__()} | Letzte Sicherung: {self.letzte_sicherung}"


class LegacyServer(Server):
    def __init__(
        self,
        name: str,
        ip: str,
        cpu_load: int,
        status: ServerStatusEnum,
        patch_stand: str,
    ) -> None:
        super().__init__(name, ip, "Legacy", cpu_load, status)
        self._patch_stand = patch_stand

    @property
    def patch_stand(self) -> str:
        return self._patch_stand

    def ist_kritisch(self) -> bool:
        return not self.ist_offline() and self.cpu_load >= LEGACY_WARNGRENZE

    def __str__(self) -> str:
        return f"{super().__str__()} | Patch-Stand: {self.patch_stand}"

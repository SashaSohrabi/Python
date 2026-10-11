# pyright: strict
"""Base server model with validation and database-row conversion."""

from collections.abc import Mapping

from ..constants.settings import CPU_WARNING_THRESHOLD
from ..types.server_row import ServerRow
from ..types.server_status import ServerStatusEnum
from .validation import (
    get_integer_field,
    get_text_field,
    validate_cpu_load,
    validate_status,
)


class Server:
    def __init__(
        self, name: str, ip: str, role: str, cpu_load: int,
        status: ServerStatusEnum,
    ) -> None:
        self._name = name
        self._ip = ip
        self._role = role
        self.cpu_load = cpu_load
        self.status = status

    @property
    def name(self) -> str:
        return self._name

    @property
    def ip(self) -> str:
        return self._ip

    @property
    def role(self) -> str:
        return self._role

    @property
    def cpu_load(self) -> int:
        return self._cpu_load

    @cpu_load.setter
    def cpu_load(self, value: int) -> None:
        self._cpu_load = validate_cpu_load(value)

    @property
    def status(self) -> ServerStatusEnum:
        return self._status

    @status.setter
    def status(self, value: ServerStatusEnum) -> None:
        self._status = validate_status(value)

    def is_offline(self) -> bool:
        return self.status is ServerStatusEnum.OFFLINE

    def is_critical(self) -> bool:
        return not self.is_offline() and self.cpu_load > CPU_WARNING_THRESHOLD

    def diagnostic_message(self) -> str:
        if self.is_offline():
            return f"{self.name}: Offline - server is unavailable."
        if self.is_critical():
            return f"{self.name}: Warning - CPU load is {self.cpu_load}%."
        return f"{self.name}: Online - running steadily at {self.cpu_load}% CPU load."

    def to_row(self) -> ServerRow:
        return {
            "server_type": type(self).__name__,
            "name": self.name,
            "ip": self.ip,
            "role": self.role,
            "cpu": self.cpu_load,
            "status": self.status.value,
        }

    @classmethod
    def from_row(cls, row: Mapping[str, object]) -> "Server":
        return cls(
            get_text_field(row, "name"), get_text_field(row, "ip"),
            get_text_field(row, "role"), get_integer_field(row, "cpu"),
            ServerStatusEnum(get_text_field(row, "status")),
        )

    def __str__(self) -> str:
        return (
            f"{self.name} ({self.role}) - CPU {self.cpu_load} %"
            f" - {self.status.value}"
        )

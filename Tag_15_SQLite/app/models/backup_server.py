# pyright: strict
"""Backup server model with its retention-start date."""

from collections.abc import Mapping

from ..constants.settings import BACKUP_WARNING_THRESHOLD
from ..types.server_row import ServerRow
from ..types.server_status import ServerStatusEnum
from .server import Server
from .validation import get_integer_field, get_text_field


class BackupServer(Server):
    def __init__(
        self, name: str, ip: str, cpu_load: int,
        status: ServerStatusEnum, since: str,
    ) -> None:
        super().__init__(name, ip, "Backup", cpu_load, status)
        self._since = since

    @property
    def since(self) -> str:
        return self._since

    def is_critical(self) -> bool:
        return self.is_offline() or self.cpu_load > BACKUP_WARNING_THRESHOLD

    def to_row(self) -> ServerRow:
        row = super().to_row()
        row["since"] = self.since
        return row

    @classmethod
    def from_row(cls, row: Mapping[str, object]) -> "BackupServer":
        return cls(
            get_text_field(row, "name"), get_text_field(row, "ip"),
            get_integer_field(row, "cpu"),
            ServerStatusEnum(get_text_field(row, "status")),
            get_text_field(row, "since"),
        )

    def __str__(self) -> str:
        return f"{super().__str__()} (since: {self.since})"

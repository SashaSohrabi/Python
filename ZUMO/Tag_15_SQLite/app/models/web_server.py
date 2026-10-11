# pyright: strict
"""Web server model with framework-specific warning thresholds."""

from collections.abc import Mapping

from ..constants.settings import BETA_WARNING_THRESHOLD, WEB_WARNING_THRESHOLD
from ..types.server_row import ServerRow
from ..types.server_status import ServerStatusEnum
from .server import Server
from .validation import get_integer_field, get_text_field


class WebServer(Server):
    def __init__(
        self, name: str, ip: str, cpu_load: int,
        status: ServerStatusEnum, framework: str,
    ) -> None:
        super().__init__(name, ip, "Web", cpu_load, status)
        self._framework = framework

    @property
    def framework(self) -> str:
        return self._framework

    def is_critical(self) -> bool:
        return (
            self.is_offline()
            or (self.framework == "beta" and self.cpu_load > BETA_WARNING_THRESHOLD)
            or self.cpu_load > WEB_WARNING_THRESHOLD
        )

    def to_row(self) -> ServerRow:
        row = super().to_row()
        row["framework"] = self.framework
        return row

    @classmethod
    def from_row(cls, row: Mapping[str, object]) -> "WebServer":
        return cls(
            get_text_field(row, "name"), get_text_field(row, "ip"),
            get_integer_field(row, "cpu"),
            ServerStatusEnum(get_text_field(row, "status")),
            get_text_field(row, "framework"),
        )

    def __str__(self) -> str:
        return f"{super().__str__()} (Framework: {self.framework})"

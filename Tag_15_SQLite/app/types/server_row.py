# pyright: strict
"""The row representation: base fields plus optional additional columns."""

from typing import NotRequired, TypedDict


class ServerRow(TypedDict):
    server_type: str
    name: str
    ip: str
    role: str
    cpu: int
    status: str
    framework: NotRequired[str]
    since: NotRequired[str]

# pyright: strict
"""Allowed server states; models accept only this enum."""

from enum import Enum


class ServerStatusEnum(Enum):
    ONLINE = "online"
    OFFLINE = "offline"


def validate_status(value: object) -> ServerStatusEnum:
    """Validate the enum type at runtime as well as during static checking."""
    if not isinstance(value, ServerStatusEnum):
        raise TypeError("status must be a ServerStatusEnum")
    return value

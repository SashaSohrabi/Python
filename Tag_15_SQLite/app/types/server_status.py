# pyright: strict
"""Allowed server states; models accept only this enum."""

from enum import Enum


class ServerStatusEnum(Enum):
    ONLINE = "online"
    OFFLINE = "offline"

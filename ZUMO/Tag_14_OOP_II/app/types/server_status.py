# Skriptname: server_status.py
# Autor: Sasha Sohrabi
# Datum: 29.09.2026
# Zweck: Die beiden gültigen Serverzustände festlegen.

from enum import Enum


class ServerStatusEnum(Enum):
    ONLINE = "online"
    OFFLINE = "offline"

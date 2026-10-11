from typing import Literal, TypedDict


class DatenbankServer(TypedDict):
    ip: str
    rolle: str
    cpu_load: int
    status: Literal["online", "offline"]

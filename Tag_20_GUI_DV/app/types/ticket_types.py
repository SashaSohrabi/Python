# pyright: strict
from typing import Literal, TypedDict

type TicketStatus = Literal["open", "completed"]
type TicketFilter = Literal["all", "open", "completed"]
# Each starter row contains a title, status and priority.
type TicketSeed = tuple[str, TicketStatus, int]


class Ticket(TypedDict):
    id: int
    title: str
    status: TicketStatus
    priority: int

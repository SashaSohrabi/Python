# pyright: strict
"""Simple ticket fields, allowed statuses and SQL ordering choices."""

from typing import Literal, TypedDict

type TicketStatus = Literal["open", "completed"]
# Each starter row contains a title, status and priority.
type TicketSeed = tuple[str, TicketStatus, int]
type TicketOrder = Literal["id", "priority, id"]


class Ticket(TypedDict):
    id: int
    title: str
    status: TicketStatus
    priority: int

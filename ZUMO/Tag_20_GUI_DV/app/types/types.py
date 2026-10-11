# pyright: strict
from collections.abc import Callable
from typing import Literal, TypedDict, cast

import flet as ft

# Ticket types
type TicketStatus = Literal["open", "completed"]
type TicketFilter = Literal["all", "open", "completed"]
# Each starter row contains a title, status and priority.
type TicketSeed = tuple[str, TicketStatus, int]


class Ticket(TypedDict):
    id: int
    title: str
    status: TicketStatus
    priority: int


# UI state types
class TicketListState(TypedDict):
    tickets: list[Ticket]
    status_filter: TicketFilter
    revision: int
    error: str | None


class TicketFormState(TypedDict):
    title: str
    priority: str
    title_error: str | None
    priority_error: str | None
    save_error: str | None


# Flet state types and typed hook helper
type StateSetter[T] = Callable[[T], None]


def use_state[T](initial: T | Callable[[], T]) -> tuple[T, StateSetter[T]]:
    hook = cast(
        Callable[[T | Callable[[], T]], tuple[T, StateSetter[T]]],
        getattr(ft, "use_state"),  # noqa: B009
    )
    return hook(initial)

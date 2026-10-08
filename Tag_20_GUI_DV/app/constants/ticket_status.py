# pyright: strict
from typing import Final

from ..types.ticket_types import TicketFilter, TicketStatus

STATUS_OPEN: Final[TicketStatus] = "open"
STATUS_COMPLETED: Final[TicketStatus] = "completed"
FILTER_ALL: Final[TicketFilter] = "all"

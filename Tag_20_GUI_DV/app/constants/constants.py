# pyright: strict
from pathlib import Path
from typing import Final

from ..types.types import TicketFilter, TicketStatus

# Application settings
DB: Final[Path] = Path(__file__).resolve().parents[2] / "tickets.db"
APP_TITLE: Final[str] = "Support Ticket Manager"
APP_SUBTITLE: Final[str] = "Create, prioritize, and track support tickets."
PAGE_PADDING: Final[int] = 40
RUN_IN_BROWSER: Final[bool] = False
WEB_PORT: Final[int] = 3000

# Priority limits
MIN_PRIORITY: Final[int] = 1
MAX_PRIORITY: Final[int] = 3

# Ticket status and filters
STATUS_OPEN: Final[TicketStatus] = "open"
STATUS_COMPLETED: Final[TicketStatus] = "completed"
FILTER_ALL: Final[TicketFilter] = "all"

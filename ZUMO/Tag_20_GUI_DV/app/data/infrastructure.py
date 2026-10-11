# pyright: strict
from typing import Final

from ..constants.constants import STATUS_COMPLETED, STATUS_OPEN
from ..types.types import TicketSeed

SAMPLE_TICKETS: Final[tuple[TicketSeed, ...]] = (
    ("Printer on the 2nd floor is jammed", STATUS_OPEN, 2),
    ("Software installation requested", STATUS_OPEN, 3),
    ("Reset password", STATUS_OPEN, 1),
    ("Monitor flickers", STATUS_COMPLETED, 1),
    ("Backup job failed", STATUS_OPEN, 3),
    ("Check VPN connection", STATUS_COMPLETED, 2),
)

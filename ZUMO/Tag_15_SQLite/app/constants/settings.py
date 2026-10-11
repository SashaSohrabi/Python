# pyright: strict
"""Database path and warning thresholds."""

from pathlib import Path
from typing import Final

DB: Final[Path] = Path(__file__).resolve().parents[2] / "register.db"
CPU_WARNING_THRESHOLD: Final[int] = 80
WEB_WARNING_THRESHOLD: Final[int] = 70
BETA_WARNING_THRESHOLD: Final[int] = 40
BACKUP_WARNING_THRESHOLD: Final[int] = 95

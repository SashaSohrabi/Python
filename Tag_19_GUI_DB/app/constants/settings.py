# pyright: strict
"""Paths and application settings, independent of the working directory."""

from pathlib import Path
from typing import Final

DB: Final[Path] = Path(__file__).resolve().parents[2] / "tickets.db"
APP_TITLE: Final[str] = "GUI Meets Database"
PAGE_PADDING: Final[int] = 40
MIN_PRIORITY: Final[int] = 1
MAX_PRIORITY: Final[int] = 3
RUN_IN_BROWSER: Final[bool] = False
WEB_PORT: Final[int] = 8550

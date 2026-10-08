# pyright: strict
import argparse
import sqlite3
from functools import partial
from pathlib import Path
from typing import cast

import flet as ft

from .constants.constants import DB, RUN_IN_BROWSER, WEB_PORT
from .data.database import initialize_database
from .models.ticket_register import TicketRegister
from .views.ticket_app import show_ticket_app


def parse_arguments() -> Path:
    parser = argparse.ArgumentParser(description="Exercise 29: Ticket Tool Expansion")
    parser.add_argument(
        "--db",
        type=Path,
        default=DB,
        help="Database path; use --db without a path for the terminal smoke test",
    )
    database_path = cast(Path, parser.parse_args().db)
    return database_path.expanduser().resolve()


def main() -> None:
    parsed_database_path = parse_arguments()
    try:
        initialize_database(parsed_database_path)
        register = TicketRegister(parsed_database_path)
    except (OSError, sqlite3.Error, TypeError, ValueError) as error:
        raise SystemExit(f"Database error: {error}") from error

    page_handler = partial(show_ticket_app, register=register)

    if RUN_IN_BROWSER:
        ft.run(page_handler, view=ft.AppView.WEB_BROWSER, port=WEB_PORT)
    else:
        ft.run(page_handler)

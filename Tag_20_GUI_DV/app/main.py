# pyright: strict
import argparse
import sqlite3
from pathlib import Path
from typing import cast

import flet as ft

from .constants.settings import DB, RUN_IN_BROWSER, WEB_PORT
from .data.database import initialize_database
from .services.ticket_register import TicketRegister
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

    def show_app(page: ft.Page) -> None:
        show_ticket_app(page, register)

    if RUN_IN_BROWSER:
        ft.run(show_app, view=ft.AppView.WEB_BROWSER, port=WEB_PORT)
    else:
        ft.run(show_app)

import sqlite3
from pathlib import Path
from typing import cast

DB: Path = Path(__file__).resolve().with_name("wiederholung.db")

type TicketData = tuple[str, int, str]

SAMPLE_TICKETS: list[TicketData] = [
    ("Printer issue", 2, "offen"),
    ("Update server", 1, "offen"),
    ("Create user account", 3, "offen"),
    ("Check backup", 1, "offen"),
    ("Configure router", 2, "geschlossen"),
    ("Install software", 3, "geschlossen"),
]


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DB)
    connection.row_factory = sqlite3.Row
    return connection


def create_table() -> None:
    connection = get_connection()

    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                priority INTEGER NOT NULL,
                status TEXT NOT NULL
            )
            """
        )
        connection.commit()

    except sqlite3.Error as error:
        connection.rollback()
        raise RuntimeError(
            "Could not create the tickets table."
        ) from error  # TODO: Investigate
    finally:
        connection.close()


def insert_sample_data() -> None:
    connection = get_connection()

    tickets: list[TicketData] = SAMPLE_TICKETS

    try:
        connection.executemany(
            """
            INSERT INTO tickets (title, priority, status)
            VALUES (?, ?, ?)
            """,
            tickets,
        )
        connection.commit()

    except sqlite3.Error as error:
        connection.rollback()
        raise RuntimeError(
            "Could not insert the sample tickets."
        ) from error
    finally:
        connection.close()


def get_existing_tickets() -> list[TicketData]:
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT title, priority, status
            FROM tickets
            ORDER BY id
            """
        )

        rows = cursor.fetchall()

        tickets: list[TicketData] = []

        for row in rows:
            title = cast(str, row["title"])
            priority = cast(int, row["priority"])
            status = cast(str, row["status"])

            tickets.append((title, priority, status))

        return tickets

    except sqlite3.Error as error:
        raise RuntimeError("Could not retrieve the existing tickets.") from error

    finally:
        connection.close()


def sample_data_matches() -> bool:
    existing_tickets = get_existing_tickets()
    return existing_tickets == SAMPLE_TICKETS


def initialize_database() -> None:
    create_table()

    existing_tickets = get_existing_tickets()

    if not existing_tickets:
        insert_sample_data()
        return

    if existing_tickets != SAMPLE_TICKETS:
        raise RuntimeError("The tickets table already contains different data.")


def main() -> None:
    initialize_database()


if __name__ == "__main__":
    main()

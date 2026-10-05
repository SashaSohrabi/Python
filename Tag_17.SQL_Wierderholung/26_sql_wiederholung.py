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
        raise RuntimeError("Could not create the tickets table.") from error
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
        raise RuntimeError("Could not insert the sample tickets.") from error
    finally:
        connection.close()


def convert_rows_to_tickets(rows: list[sqlite3.Row]) -> list[TicketData]:
    tickets: list[TicketData] = []

    for row in rows:
        title = cast(str, row["title"])
        priority = cast(int, row["priority"])
        status = cast(str, row["status"])

        tickets.append((title, priority, status))

    return tickets


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

        rows: list[sqlite3.Row] = cursor.fetchall()
        return convert_rows_to_tickets(rows)

    except sqlite3.Error as error:
        raise RuntimeError("Could not retrieve the existing tickets.") from error

    finally:
        connection.close()


def sample_data_matches() -> bool:
    existing_tickets = get_existing_tickets()
    return existing_tickets == SAMPLE_TICKETS


def initialize_database() -> None:
    create_table()

    if not get_existing_tickets():
        insert_sample_data()


def get_tickets_by_status(status: str, minimum_priority: int = 0) -> list[TicketData]:
    connection = get_connection()
    try:
        rows: list[sqlite3.Row] = connection.execute(
            """
            SELECT title, priority, status
            FROM tickets
            WHERE status = ? AND priority >= ?
            ORDER BY priority DESC, id ASC
            """,
            (status, minimum_priority),
        ).fetchall()

        return convert_rows_to_tickets(rows)
    except sqlite3.Error as error:
        raise RuntimeError("Could not retrieve tickets by status.") from error
    finally:
        connection.close()


def print_tickets(tickets: list[TicketData]) -> None:
    print("title | priority | status")
    if not tickets:
        print("Keine passenden Tickets.")
    for title, priority, status in tickets:
        print(f"{title} | {priority} | {status}")


def close_ticket_by_title(title: str) -> int:
    connection = get_connection()
    try:
        cursor = connection.execute(
            "UPDATE tickets SET status = ? WHERE title = ?", ("zu", title)
        )
        connection.commit()
        return cursor.rowcount
    except sqlite3.Error as error:
        connection.rollback()
        raise RuntimeError("Could not close the ticket.") from error
    finally:
        connection.close()


def main() -> None:
    initialize_database()

    print("Offene Tickets mit Prioritaet >= 2")
    print_tickets(get_tickets_by_status("offen", 2))
    print("Drucker-Ticket abschliessen")
    changed_rows = close_ticket_by_title("Printer issue")
    print("geänderte Zeilen:", changed_rows)
    print("Tickets mit Status 'zu' (nach commit erneut gelesen):")
    print_tickets(get_tickets_by_status("zu"))
    print("Offene Tickets mit Prioritaet >= 2 nach dem UPDATE:")
    print_tickets(get_tickets_by_status("offen", 2))

    print("\nZusatzaufgabe: Geschlossene Tickets mit Prioritaet >= 2")
    print_tickets(get_tickets_by_status("geschlossen", 2))


if __name__ == "__main__":
    main()

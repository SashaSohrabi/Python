from typing import cast

import psycopg
from psycopg.rows import DictRow, dict_row
from ticket_common import SAMPLE_TICKETS, TicketData, print_tickets


def get_connection() -> psycopg.Connection[DictRow]:
    return psycopg.Connection[DictRow].connect(
        host="localhost",
        port=5432,
        dbname="test_database",
        user="sasha",
        row_factory=dict_row,
    )


def create_table() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                title TEXT NOT NULL,
                priority INTEGER NOT NULL,
                status TEXT NOT NULL
            )
            """
        )


def insert_sample_data() -> None:
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.executemany(
            """
            INSERT INTO tickets (title, priority, status)
            VALUES (%s, %s, %s)
            """,
            SAMPLE_TICKETS,
        )


def convert_rows_to_tickets(rows: list[DictRow]) -> list[TicketData]:
    tickets: list[TicketData] = []

    for row in rows:
        title = cast(str, row["title"])
        priority = cast(int, row["priority"])
        status = cast(str, row["status"])

        tickets.append((title, priority, status))

    return tickets


def get_existing_tickets() -> list[TicketData]:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            SELECT title, priority, status
            FROM tickets
            ORDER BY id
            """
        )
        return convert_rows_to_tickets(cursor.fetchall())


def sample_data_matches() -> bool:
    return get_existing_tickets() == SAMPLE_TICKETS


def initialize_database() -> None:
    create_table()

    if not get_existing_tickets():
        insert_sample_data()


def get_tickets_by_status(status: str, minimum_priority: int = 0) -> list[TicketData]:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            SELECT title, priority, status
            FROM tickets
            WHERE status = %s AND priority >= %s
            ORDER BY priority DESC, id ASC
            """,
            (status, minimum_priority),
        )
        return convert_rows_to_tickets(cursor.fetchall())


def close_ticket_by_title(title: str) -> int:
    with get_connection() as connection:
        cursor = connection.execute(
            "UPDATE tickets SET status = %s WHERE title = %s", ("zu", title)
        )
        return cursor.rowcount


def main() -> None:
    initialize_database()

    print("Open tickets with priority >= 2")
    print_tickets(get_tickets_by_status("offen", 2))

    print("Closing the printer ticket")
    changed_rows = close_ticket_by_title("Printer issue")
    print("Changed rows:", changed_rows)

    print("Tickets with status 'zu' after committing the update:")
    print_tickets(get_tickets_by_status("zu"))

    print("Open tickets with priority >= 2 after the update:")
    print_tickets(get_tickets_by_status("offen", 2))

    print("\nClosed tickets with priority >= 2")
    print_tickets(get_tickets_by_status("geschlossen", 2))


if __name__ == "__main__":
    main()

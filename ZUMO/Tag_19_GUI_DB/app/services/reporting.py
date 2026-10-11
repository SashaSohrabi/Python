# pyright: strict
from collections.abc import Sequence

from ..types.ticket_types import Ticket
from .ticket_register import TicketRegister


def format_ticket(ticket: Ticket) -> str:
    return f"{ticket['id']:>4}  {ticket['title']:<32}  {ticket['status']:<8}"


def print_tickets(tickets: Sequence[Ticket]) -> None:
    print(f"connect -> fetchall: {len(tickets)} rows, 4 columns per row")
    print("Columns: id, title, status, priority")
    for ticket in tickets:
        print(f"{format_ticket(ticket)}  Priority {ticket['priority']}")
    if not tickets:
        print("No tickets found.")


def run_database_demo(register: TicketRegister) -> None:
    print(f"Database: {register.db_path}")
    print_tickets(register.get_all_tickets())
    new_id = register.create_ticket("Printer on the 3rd floor is jammed", 2)
    print(f"Form: create_ticket(...) -> ID {new_id} (assigned by SQLite)")
    print("Read again after commit():")
    print_tickets(register.get_all_tickets())

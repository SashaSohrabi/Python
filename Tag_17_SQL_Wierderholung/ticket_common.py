type TicketData = tuple[str, int, str]

SAMPLE_TICKETS: list[TicketData] = [
    ("Printer issue", 2, "offen"),
    ("Update server", 1, "offen"),
    ("Create user account", 3, "offen"),
    ("Check backup", 1, "offen"),
    ("Configure router", 2, "geschlossen"),
    ("Install software", 3, "geschlossen"),
]


def print_tickets(tickets: list[TicketData]) -> None:
    print("title | priority | status")

    if not tickets:
        print("Keine passenden Tickets.")

    for title, priority, status in tickets:
        print(f"{title} | {priority} | {status}")
# pyright: strict
"""Run the SQLite server-register demo using separate model and SQL modules."""

import argparse
from pathlib import Path

from .constants.settings import DB
from .data.database import initialize_database
from .data.infrastructure import sample_servers
from .services.reporting import assert_round_trip, format_register_report
from .services.server_register import ServerRegister


class CliArguments(argparse.Namespace):
    def __init__(self):
        super().__init__()
        self.db: Path = DB


def run_assignment(db: Path) -> None:
    servers = sample_servers()
    assert_round_trip(servers)
    print("Part 1: Round-trip checks passed for all three server types.")
    initialize_database(db)
    register = ServerRegister(db)
    inserted_count = register.insert_new_servers(servers)
    print(f"Table 'server' is ready. Database: {db}")
    print(
        f"Inserted: {inserted_count}; existing names skipped: {len(servers) - inserted_count}."
    )
    print("\nPart 2: SELECT * FROM server (ordered by id)")
    rows = register.fetch_rows()
    if rows:
        print(" | ".join(rows[0].keys()))
    for row in rows:
        print(" | ".join(str(value) for value in row.values()))
    print("\nPart 3: Loaded objects")
    before = register.load_servers()
    assert_round_trip(before)
    for server in before:
        print(f"{type(server).__name__}: {server} | {len(server.to_row())} columns")
    print("\nPart 4: Search and update")
    print("CPU >= 80 before:", register.find_server_summaries_by_min_cpu_load(80))
    comparison = register.compare_and_or_filters()
    print("Role Database AND CPU >= 80:", comparison["AND"])
    print("Role Database OR CPU >= 80:", comparison["OR"])
    print(
        "UPDATE unknown name:",
        register.update_server_cpu_load("not-found", 55),
        "rows affected",
    )
    print(
        "UPDATE db-01 to 55:",
        register.update_server_cpu_load("db-01", 55),
        "row(s) affected",
    )
    print("CPU >= 80 after:", register.find_server_summaries_by_min_cpu_load(80))
    comparison = register.compare_and_or_filters()
    print("AND after:", comparison["AND"], "| OR after:", comparison["OR"])
    print("\nPart 5: Register report")
    print(format_register_report(register, before))
    if inserted_count < len(servers):
        print("\nExisting values were preserved when inserting.")
        print("Repeating the update to 55 may result in no changed values.")
        print("For a fresh starting state, pass a new filename with --db.")


def parse_db_path() -> Path:
    parser = argparse.ArgumentParser(description="Exercise 20: SQLite server register")
    parser.add_argument("--db", type=Path, help="Path to the SQLite database file")
    args = parser.parse_args(namespace=CliArguments())
    print(args.db)
    return args.db.expanduser().resolve()


def main() -> None:
    run_assignment(parse_db_path())

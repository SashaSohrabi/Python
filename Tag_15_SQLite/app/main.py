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
    db: Path = DB


def run_assignment(db: Path) -> None:
    servers = sample_servers()
    assert_round_trip(servers)
    print("Part 1: Round-trip checks passed for all three server types.")
    initialize_database(db)
    register = ServerRegister(db)
    inserted_count = register.insert_missing_servers(servers)
    print(f"Table 'server' is ready. Database: {db}")
    print(
        f"Inserted: {inserted_count}; existing names skipped: {len(servers) - inserted_count}."
    )
    print("\nPart 2: SELECT * FROM server (ordered by id)")
    rows = register.fetch_server_rows()
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
    print("CPU >= 80 before:", register.search_by_min_cpu(80))
    comparison = register.compare_role_and_cpu_filters()
    print("Role Database AND CPU >= 80:", comparison["AND"])
    print("Role Database OR CPU >= 80:", comparison["OR"])
    print(
        "UPDATE unknown name:", register.set_cpu_load("not-found", 55), "rows affected"
    )
    print("UPDATE db-01 to 55:", register.set_cpu_load("db-01", 55), "row(s) affected")
    print("CPU >= 80 after:", register.search_by_min_cpu(80))
    comparison = register.compare_role_and_cpu_filters()
    print("AND after:", comparison["AND"], "| OR after:", comparison["OR"])
    print("\nPart 5: Register report")
    print(format_register_report(register, before))
    if inserted_count < len(servers):
        print("\nExisting values were preserved when inserting.")
        print("Repeating the update to 55 may result in no changed values.")
        print("For a fresh starting state, pass a new filename with --db.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Exercise 20: SQLite server register")
    parser.add_argument("--db", type=Path, default=DB, help="Path to the SQLite database file")
    args = parser.parse_args(namespace=CliArguments())
    run_assignment(args.db.expanduser().resolve())

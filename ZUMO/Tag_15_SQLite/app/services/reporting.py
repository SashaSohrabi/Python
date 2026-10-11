# pyright: strict
"""Check model round trips and generate a three-part register report."""

from collections.abc import Sequence

from ..models.server import Server
from ..models.validation import get_integer_field, get_text_field
from .server_register import ServerRegister


def assert_round_trip(servers: Sequence[Server]) -> None:
    """Check that rebuilding each server preserves its row values."""
    for server in servers:
        original_row = server.to_row()
        copy = type(server).from_row(original_row)
        reconstructed_row = copy.to_row()
        assert reconstructed_row == original_row, (
            f"Reconstruction failed for {server.name}: "
            f"expected {original_row}, got {reconstructed_row}"
        )


def format_register_report(register: ServerRegister, before: Sequence[Server]) -> str:
    counts = register.count_servers_by_type()
    section1 = [f"1. Counts: {sum(counts.values())} servers"]
    section1.extend(f"   {server_type}: {count}" for server_type, count in counts.items())
    highest_load = register.fetch_server_with_highest_cpu_load()
    section2 = "2. Highest load: no servers found"
    if highest_load is not None:
        section2 = (
            f"2. Highest load: {get_text_field(highest_load, 'name')} "
            f"at {get_integer_field(highest_load, 'cpu')}% CPU"
        )
    after = register.load_servers()
    old_rows = {server.name: server.to_row() for server in before}
    new_rows = {server.name: server.to_row() for server in after}
    names = old_rows.keys() | new_rows.keys()
    changed_count = sum(old_rows.get(name) != new_rows.get(name) for name in names)
    section3 = [
        f"3. Before/after - changed rows: {changed_count}",
        "   Before:",
    ]
    section3.extend(f"   {type(server).__name__}: {server}" for server in before)
    section3.append("   After:")
    section3.extend(f"   {type(server).__name__}: {server}" for server in after)
    return "\n\n".join(("\n".join(section1), section2, "\n".join(section3)))

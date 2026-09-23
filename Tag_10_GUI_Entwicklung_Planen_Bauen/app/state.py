# Skriptname: state.py
# Autor: Sasha Sohrabi
# Datum: 23.09.2026
# Zweck: Gemeinsamer Zustand für alle UI-Module innerhalb eines Panels.

from dataclasses import dataclass, field

from app.models.server import Server


@dataclass
class AppState:
    """Hält aktuelle Inventar-, Port- und Nachrichtenwerte für alle Module zentral."""

    infrastructure: dict[str, Server] = field(default_factory=dict[str, Server])
    freigaben: dict[int, str] = field(default_factory=dict[int, str])
    port_result: str = "Noch kein Port geprüft."
    port_color: str = "#526174"
    notes: list[str] = field(default_factory=list[str])


STATE = AppState()

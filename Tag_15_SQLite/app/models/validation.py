# pyright: strict
"""Validate untrusted values at the SQLite/Python boundary."""

from collections.abc import Mapping


def get_text_field(row: Mapping[str, object], name: str) -> str:
    value = row[name]
    if not isinstance(value, str):
        raise TypeError(f"{name} must be text")
    return value


def get_integer_field(row: Mapping[str, object], name: str) -> int:
    value = row[name]
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be an integer")
    return value


def validate_cpu_load(value: object) -> int:
    # bool is a subclass of int, but is not a valid CPU measurement.
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError("cpu_load must be an integer")
    if not 0 <= value <= 100:
        raise ValueError("cpu_load must be between 0 and 100")
    return value

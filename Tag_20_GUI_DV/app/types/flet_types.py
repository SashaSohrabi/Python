# pyright: strict
from collections.abc import Callable
from typing import cast

import flet as ft

type StateSetter[T] = Callable[[T | Callable[[T], T]], None]


def use_state[T](initial: T | Callable[[], T]) -> tuple[T, StateSetter[T]]:
    # Dynamic lookup supports Flet's lazy exports and isolates its loose typing.
    hook = cast(
        Callable[[T | Callable[[], T]], tuple[T, StateSetter[T]]],
        getattr(ft, "use_state"),  # noqa: B009
    )
    return hook(initial)

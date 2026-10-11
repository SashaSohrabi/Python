from collections.abc import Callable

type Updater[T] = Callable[[T], T]
type Setter[T] = Callable[[T | Updater[T]], None]
type State[T] = tuple[T, Setter[T]]

# Decorator
from collections.abc import Callable
from functools import wraps
from time import perf_counter
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def measure_execution_time(func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    def wrap_func(*args: P.args, **kwargs: P.kwargs) -> R:
        start = perf_counter()

        try:
            return func(*args, **kwargs)
        finally:
            duration = perf_counter() - start
            print(f"{func.__name__} took {duration:.6f} seconds")

    return wrap_func


# def hello() -> None:
#     print("Hello")
# test = my_decorator(hello)
# print(test())


@measure_execution_time
def modify_string(str_param: str) -> str:
    return str_param.upper()


# print(modify_string("string"))

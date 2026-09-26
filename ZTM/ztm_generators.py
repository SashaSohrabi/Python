"""
Iterable
   └── Iterator
        └── Generator
"""

from collections.abc import Generator, Iterator

from ztm_decorators import measure_execution_time


@measure_execution_time
def make_list(num: int) -> list[int]:
    return [num for num in range(num)]


# print(make_list(1000))


@measure_execution_time
def generator_function(num: int) -> Generator[int]:
    yield from range(num)


# for item in generator_function(1000):
#     print(item)


class MyGen(Iterator[int]):
    current = 0

    def __init__(self, start: int, end: int) -> None:
        self.current = start
        self.end = end

    def __iter__(self) -> "MyGen":
        return self

    def __next__(self) -> int:
        if self.current >= self.end:
            raise StopIteration

        value = self.current
        self.current += 1
        return value


first = MyGen(3, 6)
second = MyGen(10, 12)
gen = MyGen(0, 100)
# for i in gen:
#     print(i)

# print(next(first))
# print(next(second))
# print(list(first))
# print(list(first))


def fib(number: int) -> Iterator[int]:
    a, b = 0, 1

    for _ in range(number):
        yield a
        # Evaluate the right side using old values, then assign both results.
        a, b = b, a + b


for x in fib(20):
    print(x)

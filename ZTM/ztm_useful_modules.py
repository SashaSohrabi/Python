import pdb
from collections import Counter, defaultdict
from datetime import date, time

li = [1, 2, 3, 4, 5, 6, 7, 7]
sentence = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam"
# print(Counter(li))
print(Counter(sentence))

dictionary = defaultdict(lambda: "Does not exit!", {"a": 1, "b": 2})
# print(dictionary["c"])

print(time(17, 30, 4))
print(date.today())  # noqa: DTZ011


def add(num1: int, num2: int) -> int:
    pdb.set_trace()
    return num1 + num2


add(4, 4)

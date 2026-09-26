from functools import reduce

my_list = [1, 2, 3]
your_list = (10, 20, 30)
their_list = ["first", "second", "third"]



mapped_list = list(map(lambda item: item * 2, my_list))
filtered_list = list(filter(lambda item: item % 2, my_list))
zipped_list = list(zip(my_list, your_list, their_list))
accumulator = reduce(
    lambda acc, item: acc + item, your_list, 0
)  # default value is zero

print(mapped_list)
print(filtered_list)
print(zipped_list)

print(sum(your_list, 0))
print(accumulator)

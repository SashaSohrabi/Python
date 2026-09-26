# list, set, dictionary
my_list: list[str] = []

for char in "Hello":
    my_list.append(char.upper())

# print(my_list)

letters = list("Hello".upper())

# print(letters)

char_list = [char for char in "Hello".upper()]
num_list = [num * 2 for num in range(50) if num % 2 == 0]

# print(char_list)
# print(num_list)

simple_dict: dict[str, int] = {"a": 3, "b": 4}

first_dict: dict[str, int] = {k: v**2 for k, v in simple_dict.items() if v % 2 == 0}

second_dict: dict[int, int] = {num: num**2 for num in [1, 2, 3]}

# print(first_dict)
# print(second_dict)

some_list = ["a", "b", "c", "b", "d", "m", "n", "n"]

duplicates = list({i for i in some_list if some_list.count(i) > 1})

print(duplicates)
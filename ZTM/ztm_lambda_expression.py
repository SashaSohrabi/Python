# Square
my_list = [5, 4, 3]

new_list = list(map(lambda item: item**2, my_list))

print(new_list)

# List Sorting
a = [(0, 2), (4, 3), (9, 9), (10, -1)]
a.sort(key=lambda x: x[1])

print(a)

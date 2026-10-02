from pathlib import Path

file_path = Path(__file__).with_name("test.txt")

try:
    with open(file_path, mode="a+") as my_file:
        my_file.write("hey it' me!")
        my_file.write(" 😊\n")
        my_file.seek(0)
        print(my_file.read())
except FileNotFoundError as err:
    print("File does not exits")
    print(f"{err}")
except OSError as err:
    print("File cannot be read")
    print(f"{err}")
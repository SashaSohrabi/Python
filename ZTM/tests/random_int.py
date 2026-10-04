import random

MIN_NUM = 1
MAX_NUM = 10


def run_guess(guess: int, answer: int):
    if (MIN_NUM - 1) < guess < (MAX_NUM + 1):
        if guess == answer:
            print("Well done!")
            return True
    else:
        print("Between 1 and 10!")
        return False


def main(): 
    answer = random.randint(MIN_NUM, MAX_NUM)

    while True:
        try:
            guess = int(input(f"guess a number {MIN_NUM}-{MAX_NUM}: "))
            result = run_guess(guess, answer)
            if result:
                break

        except ValueError:
            print("Enter a number!")
            continue

if __name__ == '__main__':
    main()
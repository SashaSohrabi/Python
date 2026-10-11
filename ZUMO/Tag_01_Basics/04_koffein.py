print("--- Welcome to the caffeine check ---")

name = input("What is your name? ")
caffeine_count = int(
    input("How many cups of coffee or energy drinks have you consumed today? ")
)

if caffeine_count > 5:
    print(
        f"Warning, {name}: You can probably see sounds right now. "
        "Please leave the keyboard alone!"
    )
elif caffeine_count >= 2 and caffeine_count <= 4:
    print(f"{name}, the ideal operating state for programmers has been reached!")
elif caffeine_count == 5:
    print(f"{name}, you are fully caffeinated. Proceed with caution!")
else:
    print(
        f"Warning, {name}: The system is undersupplied. "
        "A trip to the coffee machine is urgently recommended!"
    )

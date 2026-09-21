# OOP
class PlayerCharacter:
    def __init__(self, name: object, age: int) -> None:
        self.membership = True
        self.name = name
        self.age = age

    @classmethod
    def create_cumulated_instance(cls, num1: int, num2: int):
        return cls("Teddy", num1 + num2)

    @staticmethod
    def adding_things(num1: int, num2: int) -> int:
        return num1 + num2


player1 = PlayerCharacter("Player 1", 20)
player2 = PlayerCharacter("Player 2", 30)

player3 = PlayerCharacter.create_cumulated_instance(20, 10)

print(PlayerCharacter.adding_things(player1.age, player2.age))

player4: object = {"name": "Sasha", "age": 41}

print(player3.age)
print(player4["age"])
print(f"player4 name is {player4['name']}")

class User:
    def sign_in(self) -> None:
        print('User is signed in')


class Wizard(User):
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    def sign_in(self) -> None:
        print(f'Wizard with name: {self.name} is signed in')

    def attack(self) -> None:
        print(f'attacking with power {self.name}')


class Archer(User):
    def __init__(self, name: str, num_arrows: int) -> None:
        self.name = name
        self.num_arrows = num_arrows

    def attack(self) -> None:
        print(f'attacking with arrows: arrows left {self.num_arrows}')


class HybridBorg(Wizard, Archer):
    def __init__(self, name: str, age: int, num_arrows: int) -> None:
        Archer.__init__(self, name, num_arrows)
        Wizard.__init__(self, name, age)


hb1 = HybridBorg('hb1', 5, 10)

wizard1 = Wizard('Merlin', 50)
archer1 = Archer('Robin', 100)


def do_attach(obj: Wizard | Archer) -> None:
    obj.attack()


characters: list[Wizard | Archer] = [wizard1, archer1, hb1]

for itm in characters:
    do_attach(itm)

import random
import time


def erzeuge_zufallszahl(untergrenze: int, obergrenze: int) -> int:
    return random.randint(untergrenze, obergrenze)


def warte(sekunden: float):
    time.sleep(sekunden)

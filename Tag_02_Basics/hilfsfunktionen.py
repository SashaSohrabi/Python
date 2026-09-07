import random
import time


def erzeuge_zufallszahl(untergrenze, obergrenze):
    return random.randint(untergrenze, obergrenze)


def warte(sekunden):
    time.sleep(sekunden)

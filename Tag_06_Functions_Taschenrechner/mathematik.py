"""
Skript: Mathematik-Engine
Autor: Sasha Sohrabi
Datum: 11.09.2026
Zweck: Die vier Grundrechenarten als wiederverwendbare Funktionen bereitstellen.
"""


def addiere(a: float, b: float) -> float:
    return a + b


def subtrahiere(a: float, b: float) -> float:
    return a - b


def multipliziere(a: float, b: float) -> float:
    return a * b


def dividiere(a: float, b: float) -> float:
    if b == 0:
        print("Fehler: Division durch 0 ist nicht erlaubt.")
        return 0.0

    return a / b

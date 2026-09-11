"""
Skript: Zahleneingabe
Autor: Sasha Sohrabi
Datum: 11.09.2026
Zweck: Gültige Dezimalzahlen über eine wiederverwendbare Eingabefunktion einlesen.
"""


def hole_zahl(text_fuer_nutzer: str) -> float:
    while True:
        try:
            # Dezimalzahlen können mit Punkt oder Komma eingegeben werden.
            return float(input(text_fuer_nutzer).strip().replace(",", "."))
        except ValueError:
            print("Ungültige Eingabe. Bitte gib eine Zahl ein.")

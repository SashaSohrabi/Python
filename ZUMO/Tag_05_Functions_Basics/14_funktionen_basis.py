"""
Skript: Funktionen-Basics
Autor: Sasha Sohrabi
Datum: 10.09.2026
Zweck: Funktionen in Python implementieren und nutzen.
"""

NETZWERKLAST_PRO_USER = 2.5


def kalkuliere_netzwerk_last(user_anzahl: int, grundlast: float) -> float:
    return user_anzahl * NETZWERKLAST_PRO_USER + grundlast


ergebnis = kalkuliere_netzwerk_last(10, 5.5)
print(f"Die berechnete Netzwerklast beträgt: {ergebnis} Mbps")

"""
Skript: Temperatur-Filter
Autor: Sasha Sohrabi
Datum: 08.09.2026
Zweck: Filtern von kritischen Messwerten mittels List Comprehension.
"""

SCHWELLENWERT = 75
MESSWERTE = [45, 60, 78, 55, 82, 90, 30, 75, 74]

kritische_werte = [wert for wert in MESSWERTE if wert >= SCHWELLENWERT]

print(f"Alle Messwerte: {MESSWERTE}")
print(f"Kritische Warnungen: {kritische_werte}")

"""
Skript: Absturzsicherer Rechner
Autor: Sasha Sohrabi
Datum: 14.09.2026
Zweck: Zwei Zahlen dividieren und ungültige Eingaben sowie Division durch null abfangen.
"""

while True:
    try:
        eingabe1 = input("Erste Zahl (q zum Beenden): ").strip()
        if eingabe1.lower() == "q":
            break
        zahl1 = float(eingabe1.replace(",", "."))

        eingabe2 = input("Zweite Zahl (q zum Beenden): ").strip()
        if eingabe2.lower() == "q":
            break
        zahl2 = float(eingabe2.replace(",", "."))

        ergebnis = zahl1 / zahl2
    except ValueError:
        print("Fehler: Bitte gib eine gültige Zahl ein.")
    except ZeroDivisionError:
        print("Fehler: Division durch 0 ist nicht erlaubt.")
    except (EOFError, KeyboardInterrupt):
        print("\nRechner beendet.")
        break
    else:
        print(f"Ergebnis: {zahl1} / {zahl2} = {ergebnis}")

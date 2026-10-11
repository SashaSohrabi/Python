"""
Skript: Modularer Industrie-Taschenrechner
Autor: Sasha Sohrabi
Datum: 11.09.2026
Zweck: Grundrechenarten über Funktionen ausführen und den Rechenverlauf anzeigen.
"""

# Phasen 1 und 2: Funktionen aus den Modulen importieren
from eingabe import hole_zahl
from mathematik import addiere, dividiere, multipliziere, subtrahiere

VERLAUF: list[str] = []


# Phasen 3 und 4: Hauptmenü und Verlauf
while True:
    print("\n=== MODULARER TASCHENRECHNER ===")
    print("[1] Addieren (+)")
    print("[2] Subtrahieren (-)")
    print("[3] Multiplizieren (*)")
    print("[4] Dividieren (/)")
    print("[5] Beenden")
    print("[6] Verlauf anzeigen")
    print("================================")

    wahl = input("Deine Wahl: ").strip()

    if wahl == "5":
        break
    elif wahl == "6":
        print("\n=== RECHENVERLAUF ===")
        if not VERLAUF:
            print("Noch keine Rechnungen vorhanden.")
        for rechnung in VERLAUF:
            print(rechnung)
    elif wahl in ["1", "2", "3", "4"]:
        zahl1 = hole_zahl("Erste Zahl: ")
        zahl2 = hole_zahl("Zweite Zahl: ")

        if wahl == "1":
            ergebnis = addiere(zahl1, zahl2)
            operator = "+"
        elif wahl == "2":
            ergebnis = subtrahiere(zahl1, zahl2)
            operator = "-"
        elif wahl == "3":
            ergebnis = multipliziere(zahl1, zahl2)
            operator = "*"
        else:
            ergebnis = dividiere(zahl1, zahl2)
            operator = "/"
            if zahl2 == 0:
                # Die fehlgeschlagene Rechnung wird nicht im Verlauf gespeichert.
                continue

        print(f"Ergebnis: {ergebnis}")
        rechnung = f"{zahl1} {operator} {zahl2} = {ergebnis}"
        VERLAUF.append(rechnung)
    else:
        print("Ungültige Auswahl. Bitte wähle eine Zahl von 1 bis 6.")

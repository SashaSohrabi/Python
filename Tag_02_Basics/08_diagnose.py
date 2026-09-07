"""
Skript: System-Diagnose
Autor: Sasha Sohrabi
Datum: 07.09.2026
Zweck: Simuliert einen Systemstart und misst zufällige Auslastungswerte.
"""

from hilfsfunktionen import erzeuge_zufallszahl, warte

VERSION = "1.0.4"
MAX_AUSLASTUNG = 85  # Schwellenwert in Prozent


def berechne_auslastung():
    print(f"Starte Diagnose-Tool v{VERSION}...")
    warte(2)
    print("Analysiere Netzwerk-Traffic...")

    warte(1)
    aktuelle_auslastung = erzeuge_zufallszahl(1, 100)
    print(f"Gemessene Auslastung: {aktuelle_auslastung}% ")

    if aktuelle_auslastung >= MAX_AUSLASTUNG:
        print("KRITISCH: Netzwerk überlastet!")
    else:
        print("OK: System läuft stabil.")


berechne_auslastung()

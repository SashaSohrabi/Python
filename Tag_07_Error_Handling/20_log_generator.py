"""
Skript: Massen-Log-Generator
Autor: Sasha Sohrabi
Datum: 14.09.2026
Zweck: 100 zufällige Systemmeldungen erzeugen und in system_logs.txt speichern.
"""

from random import choice
from pathlib import Path

skript_pfad = Path(__file__).resolve()
skript_ordner = skript_pfad.parent
LOG_DATEI = skript_ordner / "system_logs.txt"

MELDUNGEN = {
    "INFO": "System läuft normal",
    "WARNUNG": "RAM-Auslastung hoch",
    "KRITISCH": "Datenbank nicht erreichbar",
}

try:
    with open(LOG_DATEI, "w", encoding="utf-8") as datei:
        for nummer in range(1, 101):
            stufe = choice(["INFO", "WARNUNG", "KRITISCH"])
            datei.write(f"Eintrag {nummer}: [{stufe}] {MELDUNGEN[stufe]}\n")
except OSError as fehler:
    print(f"Fehler beim Schreiben von {LOG_DATEI.name}: {fehler}")
else:
    print(f"100 Log-Einträge wurden in {LOG_DATEI.name} gespeichert.")

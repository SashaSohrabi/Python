"""
Skript: System-Log-Auditor
Autor: Sasha Sohrabi
Datum: 14.09.2026
Zweck: Systemlogs prüfen, kritische Meldungen auslagern und einen Audit-Bericht erstellen.
"""

from pathlib import Path

BASIS_ORDNER = Path(__file__).resolve().parent
LOG_DATEI = BASIS_ORDNER / "system_logs.txt"
ALARM_DATEI = BASIS_ORDNER / "kritische_alarme.txt"
REPORT_DATEI = BASIS_ORDNER / "audit_report.txt"

warnungen = 0
kritische_fehler = 0

try:
    with (
        open(LOG_DATEI, "r", encoding="utf-8") as logs,
        open(ALARM_DATEI, "a", encoding="utf-8") as alarme,
        open(REPORT_DATEI, "w", encoding="utf-8") as report,
    ):
        for zeile in logs:
            if "KRITISCH" in zeile:
                alarme.write(zeile)
                kritische_fehler += 1
            elif "WARNUNG" in zeile:
                warnungen += 1

        report.write("=== SYSTEM-AUDIT-BERICHT ===\n")
        report.write(f"Quelle: {LOG_DATEI.name}\n")
        report.write(f"Warnungen insgesamt: {warnungen}\n")
        report.write(f"Kritische Fehler in diesem Lauf: {kritische_fehler}\n")
        report.write(f"Kritische Fehler wurden nach {ALARM_DATEI.name} ausgelagert.\n")
        report.write("INFO-Einträge wurden ignoriert.\n")

    print(
        f"Audit abgeschlossen: {warnungen} Warnungen, {kritische_fehler} kritische Fehler."
    )
    print(f"Bericht gespeichert in {REPORT_DATEI.name}.")
except FileNotFoundError:
    print("WARNUNG: system_logs.txt wurde nicht gefunden.")
    print("Bitte zuerst 20_log_generator.py ausführen.")
    print("Kein neuer Audit-Bericht erstellt.")
except (OSError, UnicodeError) as fehler:
    print(f"Fehler beim Lesen oder Schreiben der Dateien: {fehler}")

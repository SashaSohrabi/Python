"""
Skript: Log-Analyzer
Autor: Sasha Sohrabi
Datum: 08.09.2026
Zweck: Filtern von kritischen Log-Einträgen mittels List Comprehension.
"""

RAW_LOGS = [
    "INFO: System boot OK",
    "WARN: RAM-Auslastung bei 85%",
    "ERROR: Datenbank-Verbindung fehlgeschlagen",
    "INFO: User 'admin' eingeloggt",
    "WARN: Latenz im Netzwerk hoch",
    "ERROR: Festplatte /dev/sda1 voll",
    "INFO: Backup erfolgreich beendet",
]

kritische_logs = [log for log in RAW_LOGS if "ERROR" in log or "WARN" in log]  # Annahme: Es gibt nur drei Log-Typen: "INFO", "WARN" und "ERROR".


kritische_logs.insert(0, "ERROR: Stromversorgung USV-1 unterbrochen")
kritische_logs.remove("ERROR: Festplatte /dev/sda1 voll")
kritische_logs.sort(reverse=True)

dashboard_ansicht = kritische_logs[0:3]

print("AKTUELLE SYSTEM-WARNHINWEISE".center(50, "-"))
for log in dashboard_ansicht:
    print(f"-> {log}")

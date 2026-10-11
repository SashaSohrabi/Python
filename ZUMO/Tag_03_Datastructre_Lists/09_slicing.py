"""
Skript: Log-Analyse via Slicing
Autor: Sasha Sohrabi
Datum: 08.09.2026
Zweck: Extraktion spezifischer Teilbereiche aus einer Systemliste.
"""

LOG_DATA = [
    "Boot",
    "Init",
    "Netzwerk_OK",
    "DB_Connect",
    "User_Login",
    "Error_404",
    "Shutdown",
]

# 1. Extrahiere die ersten drei Einträge (Index 0 bis exklusiv 3)
start_phase = LOG_DATA[0:3]
print(f"Startphase: {start_phase}")

# 2. Extrahiere die letzten beiden Einträge (Nutze negative Indizes!)
end_phase = LOG_DATA[-2:]
print(f"Endphase: {end_phase}")

# 3. Drehe die komplette Liste um (Nutze den Step-Parameter)
reverse_log = LOG_DATA[::-1]
print(f"Rückwärts: {reverse_log}")

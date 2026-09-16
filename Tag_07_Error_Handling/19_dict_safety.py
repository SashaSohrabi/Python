"""
Skript: Sicherer Dictionary-Zugriff
Autor: Sasha Sohrabi
Datum: 14.09.2026
Zweck: Fehlende Dictionary-Schlüssel mit try/except und alternativ mit .get() behandeln.
"""

server = {"ip": "10.0.0.1", "status": "online"}

# Weg 1: Der direkte Zugriff löst einen KeyError aus, den wir abfangen.
try:
    cpu_auslastung = server["cpu_auslastung"]
    print(f"CPU-Auslastung: {cpu_auslastung}")
except KeyError:
    print("Fehler: Der Schlüssel 'cpu_auslastung' ist nicht vorhanden.")

# Weg 2: .get() liefert bei einem fehlenden Schlüssel None statt eines Fehlers.
cpu_auslastung = server.get("cpu_auslastung")
print(f"CPU-Auslastung mit .get(): {cpu_auslastung}")

# Ein eigener Standardwert kann als zweites Argument angegeben werden.
cpu_anzeige = server.get("cpu_auslastung", "nicht verfügbar")
print(f"CPU-Auslastung mit Standardwert: {cpu_anzeige}")

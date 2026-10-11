"""
Skript: Server-Monitoring
Autor: Sasha Sohrabi
Datum: 09.09.2026
Zweck: Serverdaten verwalten, sicher auslesen und auf kritische CPU-Last prüfen.
"""

from typing import TypedDict


class ServerData(TypedDict):
    ip: str
    rolle: str
    cpu_load: int
    status: str


INFRASTRUKTUR: dict[str, ServerData] = {
    "web-01": {
        "ip": "192.168.1.10",
        "rolle": "Frontend",
        "cpu_load": 45,
        "status": "online",
    },
    "db-01": {
        "ip": "192.168.1.20",
        "rolle": "Datenbank",
        "cpu_load": 92,
        "status": "online",
    },
    "backup-01": {
        "ip": "192.168.1.30",
        "rolle": "Backup",
        "cpu_load": 0,
        "status": "offline",
    },
}

datenbank_ip = INFRASTRUKTUR["db-01"]["ip"]
print(f"Die Datenbank ist erreichbar unter: {datenbank_ip}")

INFRASTRUKTUR["backup-01"]["status"] = "online"
print(f"Neuer Status von backup-01: {INFRASTRUKTUR['backup-01']['status']}")

INFRASTRUKTUR["cache-01"] = {
    "ip": "192.168.1.40",
    "rolle": "Cache",
    "cpu_load": 25,
    "status": "online",
}

temperatur = INFRASTRUKTUR["web-01"].get("temperatur")
print(f"Temperatur von web-01: {temperatur}")

for server_name, server in INFRASTRUKTUR.items():
    print(f"Überprüfung von {server_name}:".center(50, "-"))
    if server["status"] == "offline":
        print(f"OFFLINE: {server_name} ist aktuell nicht erreichbar.")
    elif server["status"] == "online" and server["cpu_load"] > 80:
        print(f"WARNUNG: {server_name} ist überlastet ({server['cpu_load']}%)!")
    else:
        print(f"OK: {server_name} läuft stabil.")

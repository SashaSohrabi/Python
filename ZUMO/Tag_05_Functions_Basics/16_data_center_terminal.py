"""
Skript: Data-Center-Terminal
Autor: Sasha Sohrabi
Datum: 10.09.2026
Zweck: Menübasierte Serververwaltung mit Auflistung, simuliertem Ping,
       Statusumschaltung und Registrierung neuer Server.
"""

SERVERS: dict[str, dict[str, str]] = {
    "SRV-WEB-01": {"ip": "192.168.10.10", "status": "online", "os": "Linux"},
    "SRV-WEB-02": {"ip": "192.168.10.11", "status": "offline", "os": "Linux"},
    "SRV-DB-01": {"ip": "192.168.10.20", "status": "online", "os": "Windows"},
}


def zeige_alle_server():
    for name, daten in SERVERS.items():
        print(f"[{daten['status'].upper()}] {name} ({daten['os']}) - {daten['ip']}")


def ping_server(server_name: str):
    server = SERVERS.get(server_name)

    if server is None:
        print("Fehler: Server existiert nicht.")
        return

    message = (
        "Erfolgreich: Ping beantwortet."
        if server["status"] == "online"
        else "Timeout: Server nicht erreichbar."
    )
    print(message)


def status_umschalten(server_name: str):
    server = SERVERS.get(server_name)

    if server is None:
        print("Fehler: Server existiert nicht.")
        return

    server["status"] = "offline" if server["status"] == "online" else "online"

    print(f"Status von {server_name} wurde auf {server['status']} gesetzt.")


def server_hinzufuegen(name: str, ip: str, os: str):
    if name in SERVERS:
        print("Fehler: Server existiert bereits.")
        return

    SERVERS[name] = {"ip": ip, "status": "offline", "os": os}
    print(f"Server {name} wurde hinzugefügt.")


while True:
    print("\n=== DATA CENTER TERMINAL ===")
    print("[1] Alle Server auflisten")
    print("[2] Einzelnen Server anpingen")
    print("[3] Server-Status umschalten (Ein/Aus)")
    print("[4] Neuen Server registrieren")
    print("[5] Terminal beenden")
    print("============================")

    wahl = input("Deine Wahl: ").strip()

    if wahl == "1":
        zeige_alle_server()
    elif wahl == "2":
        server_name = input("Servername: ").strip()
        ping_server(server_name)
    elif wahl == "3":
        server_name = input("Servername: ").strip()
        status_umschalten(server_name)
    elif wahl == "4":
        name = input("Servername: ").strip()
        ip = input("IP-Adresse: ").strip()
        betriebssystem = input("Betriebssystem: ").strip()
        server_hinzufuegen(name, ip, betriebssystem)
    elif wahl == "5":
        break
    else:
        print("Ungültige Auswahl. Bitte wähle eine Zahl von 1 bis 5.")

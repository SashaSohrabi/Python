"""CRUD: Server erstellen, anzeigen, bearbeiten und löschen."""

from ipaddress import ip_address

from farben import Farbe
from log_level import LogLevel
from logger import schreibe_log
from server_modell import DatenbankServer, Server, Webserver
from server_verwaltung import finde_server_nach_name, speichere_aenderung


def server_hinzufuegen(server_liste: list[Server]) -> None:
    print(f"\n{Farbe.BLAU}{' Servertyp auswählen '.center(50, '-')}{Farbe.RESET}")
    print(f"{Farbe.BLAU}1 - Generischer Server{Farbe.RESET}")
    print(f"{Farbe.BLAU}2 - Webserver{Farbe.RESET}")
    print(f"{Farbe.BLAU}3 - Datenbankserver{Farbe.RESET}")
    print(f"{Farbe.BLAU}0 - Abbrechen{Farbe.RESET}")

    try:
        server_typ = int(input("Servertyp: ").strip())
    except ValueError:
        schreibe_log(
            LogLevel.ERROR,
            "Server nicht hinzugefügt: Ganze Zahl für den Servertyp erwartet.",
            Farbe.ROT,
        )
        return

    if server_typ == 0:
        schreibe_log(LogLevel.INFO, "Hinzufügen eines Servers abgebrochen.", Farbe.BLAU)
        return

    if server_typ not in (1, 2, 3):
        schreibe_log(
            LogLevel.WARNING,
            f"Server nicht hinzugefügt: Ungültiger Servertyp {server_typ} gewählt.",
            Farbe.GELB,
        )
        return

    name = input("Servername: ").strip()
    ip = input("IP-Adresse: ").strip()
    betriebssystem = input("Betriebssystem: ").strip()

    if not name or not ip or not betriebssystem:
        schreibe_log(
            LogLevel.ERROR,
            "Server nicht hinzugefügt: Name, IP-Adresse und Betriebssystem erforderlich.",
            Farbe.ROT,
        )
        return

    for vorhandener_server in server_liste:
        if vorhandener_server.name.casefold() == name.casefold():
            schreibe_log(
                LogLevel.ERROR,
                f"Server nicht hinzugefügt: Name {name} bereits vergeben.",
                Farbe.ROT,
            )
            return

    try:
        ip_adresse = ip_address(ip)
    except ValueError:
        schreibe_log(
            LogLevel.ERROR,
            f"Server nicht hinzugefügt: Ungültige IP-Adresse {ip} erkannt.",
            Farbe.ROT,
        )
        return

    for vorhandener_server in server_liste:
        if ip_address(vorhandener_server.ip) == ip_adresse:
            schreibe_log(
                LogLevel.ERROR,
                f"Server nicht hinzugefügt: IP-Adresse {ip} bereits "
                f"Server {vorhandener_server.name} zugewiesen.",
                Farbe.ROT,
            )
            return

    server: Server
    if server_typ == 1:
        server = Server(name, str(ip_adresse), betriebssystem)

    elif server_typ == 2:
        domain = input("Domain: ").strip()
        if not domain:
            schreibe_log(
                LogLevel.ERROR,
                "Webserver nicht hinzugefügt: Domain erforderlich.",
                Farbe.ROT,
            )
            return

        ssl_eingabe = input("SSL aktiv? (ja/nein): ").strip().casefold()
        if ssl_eingabe not in ("ja", "nein"):
            schreibe_log(
                LogLevel.ERROR,
                "Webserver nicht hinzugefügt: ja oder nein für SSL erwartet.",
                Farbe.ROT,
            )
            return

        ssl_aktiv = ssl_eingabe == "ja"
        server = Webserver(name, str(ip_adresse), betriebssystem, domain, ssl_aktiv)

    else:
        db_typ = input("Datenbanktyp: ").strip()
        if not db_typ:
            schreibe_log(
                LogLevel.ERROR,
                "Datenbankserver nicht hinzugefügt: Datenbanktyp erforderlich.",
                Farbe.ROT,
            )
            return

        try:
            port = int(input("Port (1-65535): ").strip())
        except ValueError:
            schreibe_log(
                LogLevel.ERROR,
                "Datenbankserver nicht hinzugefügt: Ganze Zahl für den Port erwartet.",
                Farbe.ROT,
            )
            return

        if not 1 <= port <= 65535:
            schreibe_log(
                LogLevel.ERROR,
                "Datenbankserver nicht hinzugefügt: Port außerhalb von 1 bis 65535 erkannt.",
                Farbe.ROT,
            )
            return

        server = DatenbankServer(name, str(ip_adresse), betriebssystem, db_typ, port)

    server_liste.append(server)
    if not speichere_aenderung(server_liste):
        server_liste.pop()
        return
    schreibe_log(LogLevel.INFO, f"Server {server.name} hinzugefügt.", Farbe.GRUEN)


def zeige_server(server_liste: list[Server]) -> None:
    if not server_liste:
        schreibe_log(LogLevel.INFO, "Leere Serverliste angezeigt.", Farbe.BLAU)
        return

    print(f"\n{Farbe.BLAU}{' Serverliste '.center(50, '-')}{Farbe.RESET}")
    for nummer, server in enumerate(server_liste, start=1):
        details = (
            f"{nummer} - {server.name} | IP: {server.ip} | "
            f"OS: {server.os} | Status: {server.status}"
        )
        if isinstance(server, Webserver):
            ssl_status = "aktiv" if server.ssl_aktiv else "inaktiv"
            details += (
                f" | Typ: Webserver | Domain: {server.domain} | SSL: {ssl_status}"
            )
        elif isinstance(server, DatenbankServer):
            details += f" | Typ: Datenbankserver | DB-Typ: {server.db_typ} | Port: {server.port}"
        else:
            details += " | Typ: Generischer Server"
        print(f"{Farbe.GRUEN}{details}{Farbe.RESET}")
    schreibe_log(LogLevel.INFO, "Serverliste angezeigt.")


def server_loeschen(server_liste: list[Server]) -> None:
    server = finde_server_nach_name(server_liste)
    if server is None:
        return

    position = server_liste.index(server)
    server_liste.pop(position)
    if not speichere_aenderung(server_liste):
        server_liste.insert(position, server)
        return
    schreibe_log(LogLevel.INFO, f"Server {server.name} gelöscht.", Farbe.GRUEN)


def bearbeite_server_ip(server_liste: list[Server]) -> None:
    server = finde_server_nach_name(server_liste)
    if server is None:
        return

    ip = input("Neue IP-Adresse (Enter = abbrechen): ").strip()
    if not ip:
        schreibe_log(LogLevel.INFO, "IP-Bearbeitung abgebrochen.", Farbe.BLAU)
        return

    try:
        neue_ip = ip_address(ip)
    except ValueError:
        schreibe_log(
            LogLevel.ERROR,
            f"IP-Adresse nicht geändert: Ungültige IP-Adresse {ip} erkannt.",
            Farbe.ROT,
        )
        return

    for vorhandener_server in server_liste:
        if (
            vorhandener_server is not server
            and ip_address(vorhandener_server.ip) == neue_ip
        ):
            schreibe_log(
                LogLevel.ERROR,
                f"IP-Adresse nicht geändert: IP-Adresse {ip} bereits "
                f"Server {vorhandener_server.name} zugewiesen.",
                Farbe.ROT,
            )
            return

    alte_ip = server.ip
    if ip_address(alte_ip) == neue_ip:
        schreibe_log(
            LogLevel.INFO,
            f"IP-Adresse von Server {server.name} unverändert beibehalten.",
            Farbe.BLAU,
        )
        return

    server.ip = str(neue_ip)
    if not speichere_aenderung(server_liste):
        server.ip = alte_ip
        return
    schreibe_log(
        LogLevel.INFO,
        f"IP-Adresse von Server {server.name} von {alte_ip} auf {server.ip} geändert.",
        Farbe.GRUEN,
    )

from ipaddress import ip_address

from farben import Farbe
from log_level import LogLevel
from logger import analysiere_log, schreibe_log
from server_modell import DatenbankServer, Server, Webserver


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


def waehle_server(server_liste: list[Server]) -> Server | None:
    if not server_liste:
        schreibe_log(
            LogLevel.INFO,
            "Serverauswahl nicht möglich: Keine Server vorhanden.",
            Farbe.BLAU,
        )
        return None

    print(f"\n{Farbe.BLAU}{' Serverauswahl '.center(50, '-')}{Farbe.RESET}")
    for nummer, server in enumerate(server_liste, start=1):
        print(f"{Farbe.BLAU}{nummer} - {server.name}{Farbe.RESET}")

    try:
        auswahl = int(input("Servernummer (0 = abbrechen): ").strip())
    except ValueError:
        schreibe_log(
            LogLevel.ERROR,
            "Ungültige Serverauswahl erkannt: Ganze Zahl erwartet.",
            Farbe.ROT,
        )
        return None

    if auswahl == 0:
        schreibe_log(LogLevel.INFO, "Serverauswahl abgebrochen.", Farbe.BLAU)
        return None

    if 1 <= auswahl <= len(server_liste):
        return server_liste[auswahl - 1]

    schreibe_log(
        LogLevel.WARNING,
        f"Ungültige Serverauswahl erkannt: {auswahl}.",
        Farbe.GELB,
    )
    return None


def wechsle_serverstatus(server_liste: list[Server]) -> None:
    server = waehle_server(server_liste)
    if server is None:
        return

    alter_status = server.status
    server.status_wechseln()
    schreibe_log(
        LogLevel.INFO,
        f"Status von Server {server.name} von {alter_status} auf {server.status} geändert.",
        Farbe.GRUEN,
    )


def pruefe_serverstatus(server_liste: list[Server]) -> None:
    server = waehle_server(server_liste)
    if server is None:
        return

    status = "online" if server.ping() else "offline"
    schreibe_log(
        LogLevel.INFO,
        f"Status von Server {server.name} geprüft: {status}.",
        Farbe.GRUEN,
    )


def zeige_log_report() -> None:
    try:
        statistik = analysiere_log()
    except (OSError, UnicodeError) as fehler:
        schreibe_log(
            LogLevel.ERROR,
            f"Log-Report konnte nicht gelesen werden: {fehler}",
            Farbe.ROT,
        )
        return

    print(f"\n{Farbe.BLAU}{' Log-Report '.center(50, '-')}{Farbe.RESET}")
    print(f"{Farbe.GRUEN}INFO-Einträge:  {statistik[LogLevel.INFO]}{Farbe.RESET}")
    print(f"{Farbe.GRUEN}ERROR-Einträge: {statistik[LogLevel.ERROR]}{Farbe.RESET}")


def beende_programm(grund: str) -> None:
    schreibe_log(LogLevel.INFO, f"Programmbeendigung angefordert ({grund}).")
    schreibe_log(LogLevel.INFO, "Programm beendet.", Farbe.GRUEN)


def main() -> None:
    server_liste: list[Server] = []
    schreibe_log(LogLevel.INFO, "Programm gestartet.")

    try:
        while True:
            print(f"\n{Farbe.BLAU}{' DCMS Backend '.center(50, '-')}{Farbe.RESET}")
            print(f"{Farbe.BLAU}1 - Server hinzufügen{Farbe.RESET}")
            print(f"{Farbe.BLAU}2 - Server anzeigen{Farbe.RESET}")
            print(f"{Farbe.BLAU}3 - Log-Report{Farbe.RESET}")
            print(f"{Farbe.BLAU}4 - Serverstatus wechseln{Farbe.RESET}")
            print(f"{Farbe.BLAU}5 - Serverstatus prüfen{Farbe.RESET}")
            print(f"{Farbe.BLAU}0 - Programm beenden{Farbe.RESET}")

            try:
                auswahl = int(input("Auswahl: ").strip())
            except ValueError:
                schreibe_log(
                    LogLevel.ERROR,
                    "Ungültige Eingabe erkannt: Ganze Zahl erwartet.",
                    Farbe.ROT,
                )
                continue

            if auswahl == 1:
                server_hinzufuegen(server_liste)

            elif auswahl == 2:
                zeige_server(server_liste)

            elif auswahl == 3:
                zeige_log_report()

            elif auswahl == 4:
                wechsle_serverstatus(server_liste)

            elif auswahl == 5:
                pruefe_serverstatus(server_liste)

            elif auswahl == 0:
                beende_programm("Menü")
                break

            else:
                schreibe_log(
                    LogLevel.WARNING,
                    f"Ungültige Menüauswahl erkannt: {auswahl}.",
                    Farbe.GELB,
                )

    except EOFError:
        print()
        beende_programm("Ende der Eingabe (EOF)")
    except KeyboardInterrupt:
        print()
        beende_programm("Tastaturabbruch (Strg+C)")


if __name__ == "__main__":
    main()

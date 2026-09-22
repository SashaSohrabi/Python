"""Server auswählen, ihren Status verwalten und Änderungen speichern."""

from farben import Farbe
from log_level import LogLevel
from logger import schreibe_log
from server_modell import Server
from storage import daten_speichern


def speichere_aenderung(server_liste: list[Server]) -> bool:
    try:
        daten_speichern(server_liste)
    except (OSError, ValueError, TypeError) as fehler:
        schreibe_log(
            LogLevel.ERROR,
            f"Änderung nicht übernommen: Infrastruktur konnte nicht gespeichert werden: {fehler}",
            Farbe.ROT,
        )
        return False
    return True


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


def finde_server_nach_name(server_liste: list[Server]) -> Server | None:
    if not server_liste:
        schreibe_log(
            LogLevel.INFO,
            "Serversuche nicht möglich: Keine Server vorhanden.",
            Farbe.BLAU,
        )
        return None

    name = input("Servername (Enter = abbrechen): ").strip()
    if not name:
        schreibe_log(LogLevel.INFO, "Serversuche abgebrochen.", Farbe.BLAU)
        return None

    for server in server_liste:
        if server.name.casefold() == name.casefold():
            return server

    schreibe_log(LogLevel.WARNING, f"Server {name} nicht gefunden.", Farbe.GELB)
    return None


def wechsle_serverstatus(server_liste: list[Server]) -> None:
    server = waehle_server(server_liste)
    if server is None:
        return

    alter_status = server.status
    server.status_wechseln()
    if not speichere_aenderung(server_liste):
        server.status = alter_status
        return
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

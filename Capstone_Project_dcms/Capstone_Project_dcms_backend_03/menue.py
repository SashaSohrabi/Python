"""Das Terminal-Menü und den Programmablauf steuern."""

from farben import Farbe
from log_level import LogLevel
from logger import analysiere_log, schreibe_log
from server_crud import (
    bearbeite_server_ip,
    server_hinzufuegen,
    server_loeschen,
    zeige_server,
)
from server_modell import Server
from server_verwaltung import pruefe_serverstatus, wechsle_serverstatus
from storage import daten_laden, daten_speichern


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


def beende_programm(grund: str, server_liste: list[Server]) -> None:
    schreibe_log(LogLevel.INFO, f"Programmbeendigung angefordert ({grund}).")
    try:
        daten_speichern(server_liste)
    except (OSError, ValueError, TypeError) as fehler:
        schreibe_log(
            LogLevel.ERROR,
            f"Programm mit Speicherfehler beendet: {fehler}",
            Farbe.ROT,
        )
        return
    schreibe_log(LogLevel.INFO, "Infrastruktur gespeichert.")
    schreibe_log(LogLevel.INFO, "Programm beendet.", Farbe.GRUEN)


def starte_menue() -> None:
    schreibe_log(LogLevel.INFO, "Programm gestartet.")

    try:
        server_liste = daten_laden()
    except (OSError, ValueError) as fehler:
        schreibe_log(
            LogLevel.ERROR,
            f"Programmstart abgebrochen: Infrastruktur konnte nicht geladen werden: {fehler}",
            Farbe.ROT,
        )
        return
    schreibe_log(LogLevel.INFO, f"Infrastruktur geladen: {len(server_liste)} Server.")

    try:
        while True:
            print(f"\n{Farbe.BLAU}{' DCMS Backend '.center(50, '-')}{Farbe.RESET}")
            print(f"{Farbe.BLAU}1 - Server hinzufügen{Farbe.RESET}")
            print(f"{Farbe.BLAU}2 - Server anzeigen{Farbe.RESET}")
            print(f"{Farbe.BLAU}3 - Log-Report{Farbe.RESET}")
            print(f"{Farbe.BLAU}4 - Serverstatus wechseln{Farbe.RESET}")
            print(f"{Farbe.BLAU}5 - Serverstatus prüfen{Farbe.RESET}")
            print(f"{Farbe.BLAU}6 - Server löschen{Farbe.RESET}")
            print(f"{Farbe.BLAU}7 - IP-Adresse bearbeiten{Farbe.RESET}")
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

            elif auswahl == 6:
                server_loeschen(server_liste)

            elif auswahl == 7:
                bearbeite_server_ip(server_liste)

            elif auswahl == 0:
                beende_programm("Menü", server_liste)
                break

            else:
                schreibe_log(
                    LogLevel.WARNING,
                    f"Ungültige Menüauswahl erkannt: {auswahl}.",
                    Farbe.GELB,
                )

    except EOFError:
        print()
        beende_programm("Ende der Eingabe (EOF)", server_liste)
    except KeyboardInterrupt:
        print()
        beende_programm("Tastaturabbruch (Strg+C)", server_liste)

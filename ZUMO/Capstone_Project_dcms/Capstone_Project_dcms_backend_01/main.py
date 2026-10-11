from farben import Farbe
from log_level import LogLevel
from logger import analysiere_log, schreibe_log


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
    schreibe_log(LogLevel.INFO, "Programm gestartet.")

    try:
        while True:
            print(f"\n{Farbe.BLAU}{' DCMS Backend '.center(50, '-')}{Farbe.RESET}")
            print(f"{Farbe.BLAU}1 - Server hinzufügen{Farbe.RESET}")
            print(f"{Farbe.BLAU}2 - Server anzeigen{Farbe.RESET}")
            print(f"{Farbe.BLAU}3 - Log-Report{Farbe.RESET}")
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
                schreibe_log(
                    LogLevel.INFO,
                    "Hinzufügen eines Servers angefordert.",
                    Farbe.BLAU,
                )

            elif auswahl == 2:
                schreibe_log(
                    LogLevel.INFO,
                    "Anzeige der Server angefordert.",
                    Farbe.BLAU,
                )

            elif auswahl == 3:
                zeige_log_report()

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

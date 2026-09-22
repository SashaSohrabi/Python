import os
from datetime import datetime
from pathlib import Path

from farben import Farbe
from log_level import LogLevel

skript_ordner = Path(__file__).resolve().parent
LOG_DATEI = skript_ordner / "dcms_audit.log"
ALTE_LOG_DATEI = skript_ordner / "dcms_audit_old.log"
MAX_LOG_ZEILEN = 50


def rotiere_log() -> None:
    """Archiviere die aktuelle Datei, wenn sie bereits mehr als 50 Zeilen hat."""
    try:
        with open(LOG_DATEI, encoding="utf-8") as datei:
            anzahl_zeilen = sum(1 for _ in datei)
    except FileNotFoundError:
        return

    if anzahl_zeilen >= MAX_LOG_ZEILEN:
        os.replace(LOG_DATEI, ALTE_LOG_DATEI)


def schreibe_log(level: str, nachricht: str, farbe: str | None = None) -> None:
    zeitstempel = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")

    log_eintrag = f"[{zeitstempel}] [{level}] {nachricht}\n"

    try:
        rotiere_log()
        with open(LOG_DATEI, "a", encoding="utf-8") as datei:
            datei.write(log_eintrag)
    except (OSError, UnicodeError) as fehler:
        print(f"{Farbe.ROT}Log konnte nicht geschrieben werden: {fehler}{Farbe.RESET}")

    if farbe is not None:
        print(f"{farbe}{nachricht}{Farbe.RESET}")


def analysiere_log() -> dict[str, int]:
    statistik = {LogLevel.INFO: 0, LogLevel.ERROR: 0}

    try:
        with open(LOG_DATEI, encoding="utf-8") as datei:
            for zeile in datei:
                teile = zeile.split("] ", 2)
                if len(teile) != 3 or not teile[0].startswith("["):
                    continue

                level_feld = teile[1] + "]"
                for level in statistik:
                    if level_feld == f"[{level}]":
                        statistik[level] += 1
    except FileNotFoundError:
        return statistik

    return statistik

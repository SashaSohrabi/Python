import json
import os
import shutil
from ipaddress import ip_address
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import cast

from server_modell import DatenbankServer, Server, Webserver

SKRIPT_ORDNER = Path(__file__).resolve().parent
DATEI_PFAD = SKRIPT_ORDNER / "infrastruktur.json"
BACKUP_PFAD = SKRIPT_ORDNER / "infrastruktur_backup.json"


def _lese_text(daten: dict[str, object], feld: str) -> str:
    """Lies einen erforderlichen Textwert aus einem gespeicherten Server."""
    wert = daten.get(feld)
    if not isinstance(wert, str) or not wert.strip():
        raise ValueError(f"Feld '{feld}' muss einen nicht leeren Text enthalten.")
    return wert.strip()


def _server_aus_daten(daten: dict[str, object]) -> Server:
    """Prüfe die gespeicherten Attribute und stelle die passende Klasse wieder her."""
    typ = _lese_text(daten, "typ")
    name = _lese_text(daten, "name")
    ip = str(ip_address(_lese_text(daten, "ip")))
    betriebssystem = _lese_text(daten, "os")
    status = _lese_text(daten, "status")
    if status not in ("online", "offline"):
        raise ValueError("Status muss 'online' oder 'offline' sein.")

    server: Server
    if typ == "Server":
        server = Server(name, ip, betriebssystem)
    elif typ == "Webserver":
        domain = _lese_text(daten, "domain")
        ssl_aktiv = daten.get("ssl_aktiv")
        if not isinstance(ssl_aktiv, bool):
            raise ValueError("Feld 'ssl_aktiv' muss ein Boolean sein.")
        server = Webserver(name, ip, betriebssystem, domain, ssl_aktiv)
    elif typ == "DatenbankServer":
        db_typ = _lese_text(daten, "db_typ")
        port = daten.get("port")
        if (
            isinstance(port, bool)
            or not isinstance(port, int)
            or not 1 <= port <= 65535
        ):
            raise ValueError("Port muss eine ganze Zahl zwischen 1 und 65535 sein.")
        server = DatenbankServer(name, ip, betriebssystem, db_typ, port)
    else:
        raise ValueError(f"Unbekannter Servertyp: {typ}.")

    server.status = status
    return server


def _server_liste_aus_daten(daten: object) -> list[Server]:
    """Prüfe die gesamte Liste, damit keine fehlerhaften Teildaten geladen werden."""
    if not isinstance(daten, list):
        raise TypeError("Die Infrastruktur muss als JSON-Liste gespeichert sein.")

    server_liste: list[Server] = []
    namen: set[str] = set()
    ip_adressen: set[str] = set()
    for nummer, eintrag in enumerate(cast(list[object], daten), start=1):
        if not isinstance(eintrag, dict):
            raise TypeError(f"Servereintrag {nummer} muss ein JSON-Objekt sein.")
        try:
            server = _server_aus_daten(cast(dict[str, object], eintrag))
        except ValueError as fehler:
            raise ValueError(f"Servereintrag {nummer}: {fehler}") from fehler

        if server.name.casefold() in namen:
            raise ValueError(f"Servername mehrfach vorhanden: {server.name}.")
        if server.ip in ip_adressen:
            raise ValueError(f"IP-Adresse mehrfach vorhanden: {server.ip}.")
        namen.add(server.name.casefold())
        ip_adressen.add(server.ip)
        server_liste.append(server)

    return server_liste


def daten_laden() -> list[Server]:
    """Lade alle Server; eine noch nicht vorhandene Datei ergibt eine leere Liste."""
    try:
        with open(DATEI_PFAD, encoding="utf-8") as datei:
            daten = json.load(datei)
    except FileNotFoundError:
        return []

    try:
        return _server_liste_aus_daten(daten)
    except TypeError as fehler:
        raise ValueError(f"Ungültiges Dateiformat: {fehler}") from fehler


def daten_speichern(server_liste: list[Server]) -> None:
    """Sichere die bisherige Datei und ersetze sie durch die vollständigen Daten."""
    daten: list[dict[str, object]] = []
    for server in server_liste:
        eintrag: dict[str, object] = server.__dict__.copy()
        eintrag["typ"] = type(server).__name__
        daten.append(eintrag)

    _server_liste_aus_daten(daten)
    temporaere_datei: Path | None = None
    try:
        with NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=DATEI_PFAD.parent,
            prefix="infrastruktur_",
            suffix=".tmp",
            delete=False,
        ) as datei:
            temporaere_datei = Path(datei.name)
            json.dump(daten, datei, ensure_ascii=False, indent=4)
            datei.write("\n")

        if DATEI_PFAD.exists():
            shutil.copy2(DATEI_PFAD, BACKUP_PFAD)
        os.replace(temporaere_datei, DATEI_PFAD)
    finally:
        if temporaere_datei is not None:
            temporaere_datei.unlink(missing_ok=True)

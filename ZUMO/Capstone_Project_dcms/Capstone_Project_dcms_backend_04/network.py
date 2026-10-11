"""Die externe IP-Adresse des Systems über die ipify-API abfragen."""

from ipaddress import ip_address
from typing import cast

import requests

from farben import Farbe
from log_level import LogLevel
from logger import schreibe_log

IPIFY_URL = "https://api.ipify.org?format=json"
TIMEOUT_SEKUNDEN = 10


def hole_externe_ip() -> str | None:
    try:
        antwort = requests.get(IPIFY_URL, timeout=TIMEOUT_SEKUNDEN)
        antwort.raise_for_status()
    except requests.exceptions.RequestException as fehler:
        schreibe_log(
            LogLevel.ERROR,
            f"Externe IP-Adresse konnte nicht abgefragt werden: {fehler}",
            Farbe.ROT,
        )
        return None

    try:
        daten: object = antwort.json()
        if not isinstance(daten, dict):
            raise ValueError("JSON-Objekt erwartet.")

        ip = cast(dict[str, object], daten).get("ip")
        if not isinstance(ip, str) or not ip.strip():
            raise ValueError("Feld 'ip' muss einen nicht leeren Text enthalten.")

        return str(ip_address(ip.strip()))
    except ValueError as fehler:
        schreibe_log(
            LogLevel.ERROR,
            f"Ungültige Antwort von ipify: {fehler}",
            Farbe.ROT,
        )
        return None

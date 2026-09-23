# Skriptname: portcheck.py
# Autor: Sasha Sohrabi
# Datum: 23.09.2026
# Zweck: Portnummer validieren und mit der aktuellen Freigabeliste vergleichen.

from app.constants.settings import MAX_PORT, MAX_PORT_ZIFFERN, MIN_PORT
from app.data.ports import get_freigegebene_ports


def port_pruefen(
    eingabe: str, freigaben: dict[int, str] | None = None
) -> tuple[int, str | None]:
    """Prüft die Freigabeliste ohne einen Netzwerkzugriff."""
    wert = eingabe.strip()
    if not wert:
        raise ValueError("Bitte eine Portnummer eingeben.")
    # Vor int() begrenzen: Auch extrem lange Zahlen verursachen keinen Absturz.
    if len(wert) > MAX_PORT_ZIFFERN or not wert.isascii() or not wert.isdecimal():
        raise ValueError(
            f"Bitte eine Portnummer mit 1 bis {MAX_PORT_ZIFFERN} Ziffern (0–9) eingeben."
        )
    port = int(wert)
    if not MIN_PORT <= port <= MAX_PORT:
        raise ValueError(
            f"Die Portnummer muss zwischen {MIN_PORT} und {MAX_PORT} liegen."
        )
    aktuelle_freigaben = freigaben if freigaben is not None else get_freigegebene_ports()
    return port, aktuelle_freigaben.get(port)

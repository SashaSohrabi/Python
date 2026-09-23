# Skriptname: theme.py
# Autor: Sasha Sohrabi
# Datum: 23.09.2026
# Zweck: Einheitliche Farben für Oberfläche und Statusmeldungen.

from typing import Final

from app.models.status import Status

HINTERGRUND: Final[str] = "#F3F4F6"
KARTENFARBE: Final[str] = "#FFFFFF"
TEXTFARBE: Final[str] = "#172438"
NEBENTEXT: Final[str] = "#526174"
AKZENT: Final[str] = "#B5790C"
STATUSFARBEN: Final[dict[Status, str]] = {
    "ok": "#176B45",
    "warnung": "#986000",
    "fehler": "#B42332",
}

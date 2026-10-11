# Skriptname: feedback.py
# Autor: Sasha Sohrabi
# Datum: 23.09.2026
# Zweck: Statusmeldungen mit einheitlicher, typgesicherter Farbzuordnung.

import flet as ft
from app.constants.theme import STATUSFARBEN
from app.models.status import Status


def rueckmeldung(text: ft.Text, nachricht: str, status: Status) -> None:
    """Macht Meldungen durch Worte und Farbe verständlich."""
    text.value = nachricht
    text.color = STATUSFARBEN[status]

# Skriptname: status.py
# Autor: Sasha Sohrabi
# Datum: 23.09.2026
# Zweck: Erlaubte Auswertungszustände für Logik und Oberfläche.

from typing import Literal

type Status = Literal["ok", "warnung", "fehler"]

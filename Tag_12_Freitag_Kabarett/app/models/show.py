# Skriptname: show.py
# Autor: Sasha Sohrabi
# Datum: 25.09.2026
# Zweck: Ein Auftritt im Freitag-Kabarett als eigenes Objekt modellieren.

from typing import Literal


class Show:
    def __init__(
        self,
        name: str,
        kuenstler: str,
        genre: str,
        dauer_min: int,
        publikum: int,
        status: Literal["live", "pause", "next"],
    ) -> None:
        self.name = name
        self.kuenstler = kuenstler
        self.genre = genre
        self.dauer_min = dauer_min
        self.publikum = publikum
        self.status = status

    def ist_highlight(self) -> bool:
        return self.status != "pause" and self.publikum >= 80

    def __str__(self) -> str:
        zustand = {
            "live": "Live",
            "pause": "Pause",
            "next": "Als Nächstes",
        }.get(self.status, self.status)
        return (
            f"{self.name} – {self.kuenstler} ({self.genre}) – "
            f"{self.dauer_min} min – Publikum {self.publikum}% – {zustand}"
        )

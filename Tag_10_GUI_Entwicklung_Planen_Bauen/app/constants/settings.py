# Skriptname: settings.py
# Autor: Sasha Sohrabi
# Datum: 23.09.2026
# Zweck: Zentrale Anwendungswerte und fachliche Grenzen.

from typing import Final

APP_TITEL: Final[str] = "Admin-Panel"
FENSTER_BREITE: Final[int] = 940
FENSTER_HOEHE: Final[int] = 1080
SEITENABSTAND: Final[int] = 20
MODULABSTAND: Final[int] = 14
APPBAR_HOEHE: Final[int] = 60

CPU_WARNGRENZE: Final[int] = 80
MAX_HOSTNAME_LAENGE: Final[int] = 63
MIN_PORT: Final[int] = 1
MAX_PORT: Final[int] = 65535
MAX_PORT_ZIFFERN: Final[int] = 5
MAX_NOTIZEN: Final[int] = 20
MAX_NOTIZ_LAENGE: Final[int] = 280

# Unveränderliche Vorlage; jede Ansicht erzeugt daraus ihre eigene Liste.
START_NOTIZEN: Final[tuple[str, ...]] = ()

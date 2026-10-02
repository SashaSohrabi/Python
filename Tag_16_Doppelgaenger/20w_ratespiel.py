#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pyright: strict
"""Freitag 02.10. — Ratespiel mit Highscore-Datei.

Arbeitsauftrag bearbeitet: Antworten und Testergebnisse stehen am passenden Code.
Nur Standardbibliothek: Liste, Klasse, Datei.
"""

# ---- EINSTELLUNGEN: hier darfst du drehen ---------------------------------
GEHEIM: int = 42      # Teil 1: Hier steht die gesuchte Zahl.
# Teil 2: Mit MAX_RUNDEN = 3 endete das Spiel nach den falschen Tipps 1, 2, 3.
# Danach wieder auf 7 gesetzt und sieben falsche Tipps getestet.
MAX_RUNDEN: int = 7   # so viele Versuche hat man
MIN_ZAHL: int = 1     # Zahlenbereich
MAX_ZAHL: int = 100
DATEI: str = "highscore.txt"   # wo die Bestenliste gespeichert wird
# ---------------------------------------------------------------------------


class Spiel:
    """Ein Ratespiel. Merkt sich die Versuche und weiss, ob es vorbei ist."""

    def __init__(self, geheim: int, max_runden: int) -> None:
        self.geheim: int = geheim
        self.max_runden: int = max_runden
        # Teil 1: Spiel merkt sich die Tipps in self.versuche.
        # len(self.versuche) ergibt die Anzahl der bisherigen Versuche.
        self.versuche: list[int] = []

    def raten(self, zahl: int) -> str:
        """Eine Zahl prüfen und das Ergebnis als Text zurückgeben."""
        self.versuche.append(zahl)
        if zahl == self.geheim:
            return "TREFFER!"
        if zahl < self.geheim:
            return "zu klein"
        # Selbsttest 1: return liefert den Text für print(spiel.raten(tipp)).
        # Ohne dieses letzte return kommt bei einem zu grossen Tipp None zurück;
        # print zeigt dann None. Getestet mit Tipp 99 bei GEHEIM = 42.
        return "zu gross"

    def gewonnen(self) -> bool:
        # bool([]) ist False; so kommt auch vor dem ersten Tipp ein bool zurück.
        return bool(self.versuche) and self.versuche[-1] == self.geheim

    def restliche(self) -> int:
        return self.max_runden - len(self.versuche)


def highscore_lesen() -> list[tuple[str, int]]:
    """Alle gespeicherten Ergebnisse zurückgeben (Liste von Namen+Versuchen)."""
    # Jeder Eintrag ist ein Paar aus Name (str) und Versuchszahl (int).
    eintraege: list[tuple[str, int]] = []
    # Teil 4: Nur except und pass zu entfernen führt zu einem SyntaxError,
    # weil try einen except- oder finally-Block braucht. Für den Fehlertest
    # wurde auch try entfernt und die Einrückung des Leseblocks angepasst.
    # Ergebnis ohne Schutz und ohne Datei: FileNotFoundError beim Lesen.
    try:
        with open(DATEI, "r") as f:
            for zeile in f:
                teile = zeile.strip().split(";")
                if len(teile) == 2:
                    eintraege.append((teile[0], int(teile[1])))
    except FileNotFoundError:
        # Teil 4, Antwort: Ohne except bricht das Lesen einer fehlenden Datei
        # mit FileNotFoundError ab; except behandelt sie als leere Bestenliste.
        pass          # beim ersten Mal gibt es die Datei noch nicht
    return eintraege


def highscore_schreiben(name: str, versuche: int) -> None:
    """Einen neuen Eintrag anhängen."""
    with open(DATEI, "a") as f:
        f.write(f"{name};{versuche}\n")


def rangliste() -> list[tuple[str, int]]:
    """Alle Einträge, die wenigsten Versuche zuerst."""
    eintraege = highscore_lesen()
    return sorted(eintraege, key=lambda eintrag: eintrag[1])


def main() -> None:
    print("=" * 50)
    print("RATEN — finde die Zahl zwischen %d und %d" % (MIN_ZAHL, MAX_ZAHL))
    print("=" * 50)

    spiel = Spiel(GEHEIM, MAX_RUNDEN)

    # Selbsttest 2: MAX_RUNDEN = 0 erlaubt hier trotzdem einen gültigen Tipp,
    # weil die Versuchszahl erst nach dem Raten geprüft wird. Ein falscher
    # Tipp beendet das Spiel; ein Treffer gewinnt, weil dieser zuerst geprüft
    # wird. Beide Fälle wurden getestet; die Einstellung bleibt danach 7.
    while True:
        try:
            tipp = int(input("Dein Tipp: "))
        except ValueError:
            print("Keine Zahl — nochmal.")
            continue

        if not MIN_ZAHL <= tipp <= MAX_ZAHL:
            print("Bitte zwischen %d und %d." % (MIN_ZAHL, MAX_ZAHL))
            continue

        print(spiel.raten(tipp))
        if spiel.gewonnen():
            print("Gewonnen in %d Versuchen!" % len(spiel.versuche))
            break
        # Teil 1: Bei 0 oder weniger restlichen Versuchen ist das Spiel vorbei.
        # break beendet die while-Schleife; danach wird die Bestenliste gezeigt.
        if spiel.restliche() <= 0:
            print("Versuche aufgebraucht. Die Zahl war %d." % spiel.geheim)
            break
        print("Noch %d Versuche." % spiel.restliche())

    # ---- Highscore speichern ----------------------------------------------
    # Teil 1: Mit Tipp 42 gewonnen; "Sasha;1" wurde in der Datei gespeichert.
    # Teil 4: Ein Gewinn erstellt die Datei mit open(..., "a") vor dem Lesen.
    # Deshalb wurde der Fehlertest ohne Datei nach einer verlorenen Runde
    # durchgeführt. Der Schutz in highscore_lesen() ist wiederhergestellt.
    if spiel.gewonnen():
        name = input("Dein Name für die Liste: ").strip() or "unbekannt"
        highscore_schreiben(name, len(spiel.versuche))

    print()
    print("BESTENLISTE")
    platz = 1
    for name, versuche in rangliste():
        # Teil 3: Vorübergehend diese Bedingung vor print() eingesetzt:
        # if platz > 3:
        #     break
        # Testdaten: Mia (3), Noah (1), Lea (2), Ben (4), Emma (5).
        # Ausgabe: 1. Noah (1), 2. Lea (2), 3. Mia (3); die letzten zwei fehlen.
        # Danach die Bedingung wie gefordert entfernt: wieder alle Einträge.
        print("  %d. %-12s %d Versuch(e)" % (platz, name, versuche))
        platz += 1


if __name__ == "__main__":
    main()

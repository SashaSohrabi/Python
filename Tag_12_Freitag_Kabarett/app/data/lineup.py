# Skriptname: lineup.py
# Autor: Sasha Sohrabi
# Datum: 25.09.2026
# Zweck: Das Programm- und Publikumsschema des Freitag-Kabaretts erzeugen.

from app.models.show import Show


def auftritte_erzeugen() -> list[Show]:
    return [
        Show("Frau Piek – Schöne Verwirrungen", "Frau Piek", "Satire", 16, 82, "live"),
        Show("Morgenkater im Studio", "Bastian Bunt", "Sketch", 12, 74, "next"),
        Show("Der letzte Witz vor dem Abflug", "Lena Lacht", "Kabarett", 18, 91, "live"),
        Show("Kaffee, Kassensturz und Kater", "Otto Klamott", "Monolog", 10, 58, "pause"),
        Show("Bühne frei für den Nachtschreck", "Mara Mies", "Comedy", 20, 88, "next"),
    ]

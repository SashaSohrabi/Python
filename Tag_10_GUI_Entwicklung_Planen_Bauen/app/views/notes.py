# Skriptname: notes.py
# Autor: Sasha Sohrabi
# Datum: 23.09.2026
# Zweck: Notizen pro Sitzung speichern, darstellen und gemeinsam löschen.

import flet as ft
from app.components.feedback import rueckmeldung
from app.components.module_card import modul_karte
from app.constants.settings import MAX_NOTIZ_LAENGE, MAX_NOTIZEN, START_NOTIZEN
from app.constants.theme import NEBENTEXT
from app.services.notes import notiz_hinzufuegen


def modul_notizen() -> ft.Container:
    """Verwaltet Notizen in einer eigenen Liste pro geöffnetem Panel."""
    notizen: list[str] = list(START_NOTIZEN)
    eingabe = ft.TextField(
        label="Neue Notiz",
        hint_text="z. B. backup-01 prüfen und Sicherung nachholen",
        dense=True,
        multiline=True,
        min_lines=1,
        max_lines=3,
        shift_enter=True,
    )
    ergebnis = ft.Text("Noch keine Notizen gespeichert.", color=NEBENTEXT, size=13)
    notiz_liste = ft.Column(spacing=6, visible=False)
    leeren_button = ft.Button("Notizen leeren", icon=ft.Icons.DELETE_OUTLINE, disabled=True)

    def speichern() -> None:
        try:
            notiz_hinzufuegen(eingabe.value, notizen)
        except ValueError as exc:
            eingabe.error = str(exc)
            rueckmeldung(ergebnis, "Notiz wurde nicht gespeichert.", "fehler")
            return
        eingabe.error = None
        eingabe.value = ""
        notiz_liste.controls = [
            ft.Text(f"{i}. {text}", size=13) for i, text in enumerate(notizen, 1)
        ]
        notiz_liste.visible = True
        leeren_button.disabled = False
        rueckmeldung(ergebnis, f"Gespeichert. {len(notizen)} von {MAX_NOTIZEN} Notizen.", "ok")

    def leeren() -> None:
        notizen.clear()
        notiz_liste.controls.clear()
        notiz_liste.visible = False
        leeren_button.disabled = True
        rueckmeldung(ergebnis, "Alle gespeicherten Notizen dieser Sitzung wurden gelöscht.", "ok")

    eingabe.on_submit = speichern
    leeren_button.on_click = leeren
    return modul_karte(
        "04  Sitzungsnotizen",
        ft.Icons.EDIT_NOTE,
        f"Bis {MAX_NOTIZEN} Notizen mit je {MAX_NOTIZ_LAENGE} Zeichen. "
        "Nur für diese Sitzung; beim Neustart gehen sie verloren.",
        [
            eingabe,
            ft.Row(
                wrap=True,
                controls=[
                    ft.Button("Notiz speichern", icon=ft.Icons.ADD, on_click=speichern),
                    leeren_button,
                ],
            ),
            ergebnis,
            notiz_liste,
        ],
    )

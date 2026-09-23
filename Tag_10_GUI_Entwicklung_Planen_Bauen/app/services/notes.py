# Skriptname: notes.py
# Autor: Sasha Sohrabi
# Datum: 23.09.2026
# Zweck: Notizen validieren und ausschließlich nach erfolgreicher Prüfung speichern.

from app.constants.settings import MAX_NOTIZ_LAENGE, MAX_NOTIZEN


def notiz_hinzufuegen(eingabe: str, notizen: list[str]) -> str:
    """Prüft vollständig, bevor die sitzungseigene Liste verändert wird."""
    notiz = eingabe.strip()
    if not notiz:
        raise ValueError("Bitte eine Notiz eingeben.")
    if len(notiz) > MAX_NOTIZ_LAENGE:
        raise ValueError(f"Eine Notiz darf höchstens {MAX_NOTIZ_LAENGE} Zeichen enthalten.")
    if len(notizen) >= MAX_NOTIZEN:
        raise ValueError(
            f"Es sind höchstens {MAX_NOTIZEN} Notizen möglich. "
            "Bitte zuerst die gespeicherten Notizen leeren."
        )
    notizen.append(notiz)
    return notiz

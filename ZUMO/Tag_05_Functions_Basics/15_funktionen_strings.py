"""
Skript: Funktionen mit Strings
Autor: Sasha Sohrabi
Datum: 10.09.2026
Zweck: Funktionen in Python implementieren und Strings verarbeiten.
"""


def generiere_server_namen(standort: str, id: str, umgebung: str = "prod") -> str:
    return f"{standort}-{umgebung}-{id}".upper()


print(generiere_server_namen("ber", "SRV-01"))
print(generiere_server_namen("ham", "SRV-02", "test"))

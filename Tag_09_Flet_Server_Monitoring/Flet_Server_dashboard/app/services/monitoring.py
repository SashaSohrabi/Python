from app.models.server import DatenbankServer


def monitoring_status(
    infrastruktur: dict[str, DatenbankServer],
) -> tuple[str, bool]:
    warnungen: list[str] = []

    for name, daten in infrastruktur.items():
        if daten["status"] == "online" and daten["cpu_load"] > 80:
            warnungen.append(
                f"WARNUNG: {name} ist überlastet ({daten['cpu_load']} %)!"
            )

    if warnungen:
        return "\n".join(warnungen), True

    return "OK: Alle Systeme im normalen Betrieb.", False
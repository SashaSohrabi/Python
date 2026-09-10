def berechne_auslastung(wert1: float, wert2: float) -> float:
    summe = wert1 + wert2
    return round(summe, 1)


ergenbis = berechne_auslastung(45.67, 22.14)

print(f"Die Gesamtauslastung liegt bei: {ergenbis} %")
print(type(ergenbis))


# GUI-Entwicklung II: Planen & Bauen — Admin-Panel

Vier eigenständige Flet-Module für ein lokales Demo-Inventar: Serverstatus,
Hostname-Suche, Port-Freigabeliste und Sitzungsnotizen. Die Daten sind Beispiele;
das Panel führt weder Netzwerkabfragen noch echte Portscans aus.

## Auswertung der beiden PDFs

Der **Arbeitsauftrag** beschreibt die einzelnen Arbeitsschritte und Prüfungen;
die **Präsentation** erklärt dieselbe Architektur, ergänzt die Randbalken der
Karten und unterscheidet MUSS- von KANN-Anforderungen. Die Seitenangaben beziehen
sich auf die PDF-Seiten, beginnend bei 1.

| Anforderung | Quelle | Umsetzung |
| --- | --- | --- |
| Mindestens vier Module mit jeweils einem Button | Arbeitsauftrag S. 1–2; Präsentation S. 2, 4, 7 | Vier Module, fünf Buttons; Funktionsliste unten |
| Funktionsliste, GUI-Skizze und Datenmodell | Arbeitsauftrag S. 2; Präsentation S. 3–4 | Drei Planungsabschnitte in dieser Datei |
| Datei `16_admin_panel.py`, Header, klare Trennung von Konstanten, Modulen und Einstiegspunkt | Arbeitsauftrag S. 1, 3; Präsentation S. 5, 7 | Kleiner Einstiegspunkt; Konstanten, Modelle, Daten, Logik und Oberfläche in eigenen Dateien |
| Je Modul eine Funktion, die `ft.Container` zurückgibt; `main` setzt zusammen | Arbeitsauftrag S. 3; Präsentation S. 5 | `modul_dashboard`, `modul_analyzer`, `modul_portcheck`, `modul_notizen` |
| AppBar und Karten untereinander | Arbeitsauftrag S. 2–3; Präsentation S. 4 | Titel, Icons, einheitliche Karten mit Randbalken; vertikal scrollbar |
| Datenmodell als Grundlage, validierte Eingaben, sichtbare Ergebnisse | Arbeitsauftrag S. 4; Präsentation S. 7 | Typisierte Dictionaries/Listen, Prüfung vor Änderungen, Ergebnistext und Feldfehler |
| Online/Offline und CPU-Warnung oberhalb von 80 % | Arbeitsauftrag S. 4 | Offline hat Vorrang; genau 80 % ist noch ohne CPU-Warnung |
| Leere/falsche Eingaben, Riesenzahlen und Sonderzeichen prüfen | Arbeitsauftrag S. 5 | Eingabevalidierung und manuelle Prüffälle unten |
| Flet 1.0: `ft.run`, `ft.Button`, gezielte UI-Aktualisierung | Arbeitsauftrag S. 1; Präsentation S. 2, 9 | Flet-1.0-Controls; die Portkarte aktualisiert Liste, Ergebnis und Feldfehler gemeinsam nach jeder Aktion |
| Recherche zu Controls, Dialogen und `disabled` | Arbeitsauftrag S. 2–5; Präsentation S. 6, 9 | Antworten mit offiziellen Quellen unten |

Die Stumm-Buttons mit SnackBar aus Phase 2 sind ein **Zwischenstand**: In der
fertigen Fassung übernimmt jeder Button seine eigentliche Aktion. Farbige
Ergebnistexte erfüllen die Rückmeldungsanforderung aus Phase 3. Zusätzliche
Module und „Alle zurücksetzen“ sind optional; umgesetzt ist das Leeren der
Sitzungsnotizen.

## Funktionsliste

| Modul | Was tut es? | Controls | Aktion |
| --- | --- | --- | --- |
| 01 Server-Dashboard | Wertet den Status und die CPU-Last der drei Beispielserver aus. | `Container`, `Column`, `Row`, `Icon`, `Text`, `Button` | **Status aktualisieren** → Statuszeilen, Zusammenfassung und Auswertungszeit |
| 02 Hostname-Analyzer | Sucht einen Hostnamen und zeigt Rolle, IP und Status aus dem Inventar. | `TextField`, `Button`, `Text`, `ResponsiveRow` | **Server suchen** oder Enter → Treffer oder verständlicher Fehler |
| 03 Port-Freigabecheck | Erzeugt eine zufällige Freigabeliste und prüft die Portnummer gegen genau diese angezeigte Liste. | `TextField`, `Button`, `Text`, `ResponsiveRow` | **Port prüfen** oder Enter → neue Liste, danach verfügbar (grün) oder nicht verfügbar/ungültig (rot) |
| 04 Sitzungsnotizen | Speichert begrenzte Textnotizen nur für das geöffnete Panel. | mehrzeiliges `TextField`, zwei `Button`, `Text`, `Column` | **Notiz speichern**/Enter → Liste; **Notizen leeren** → leere Liste |

## GUI-Skizze

```text
+------------------------------------------------------------------+
| [Admin-Icon] Admin-Panel                                  AppBar |
+------------------------------------------------------------------+
| SYSTEMADMINISTRATION / LOKALES DEMO-INVENTAR                       |
| +--------------------------------------------------------------+ |
| | [Icon] 01 Server-Dashboard                                    | |
| | web-01 ... Online / db-01 ... Warnung / backup-01 ... Offline   | |
| | Zusammenfassung + Auswertungszeit             <--- (1)         | |
| | [1: Status aktualisieren]                                    | |
| +--------------------------------------------------------------+ |
| +--------------------------------------------------------------+ |
| | [Icon] 02 Hostname-Analyzer                                   | |
| | [Hostname: ____________________] [2: Server suchen]            | |
| | Ergebnis / Eingabefehler                      <--- (2)         | |
| +--------------------------------------------------------------+ |
| +--------------------------------------------------------------+ |
| | [Icon] 03 Port-Freigabecheck                                   | |
| | [Portnummer: __________________] [3: Port pruefen]              | |
| | Ergebnis / Eingabefehler                      <--- (3)         | |
| +--------------------------------------------------------------+ |
| +--------------------------------------------------------------+ |
| | [Icon] 04 Sitzungsnotizen                                     | |
| | [Neue Notiz: _____________________________________________]   | |
| | [4: Notiz speichern] [5: Notizen leeren]                       | |
| | Rueckmeldung + nummerierte Notizliste         <--- (4), (5)    | |
| +--------------------------------------------------------------+ |
+------------------------------------------------------------------+
```

Auf schmalen Fenstern stehen Such-/Prüfbutton und Eingabefeld untereinander.
Bei wenig Höhe wird gescrollt. Statusmeldungen enthalten neben der Farbe immer
Text: grün = unauffällig/erfolgreich, amber = CPU-Warnung, rot = Problem.

## Datenmodell und Architektur

```python
class Server(TypedDict):
    ip: str
    rolle: str
    cpu_load: int
    status: Literal["online", "offline"]

_INFRASTRUKTUR: Final[dict[str, Server]] = {
    "web-01": {
        "ip": "192.168.1.10", "rolle": "Frontend",
        "cpu_load": 45, "status": "online",
    },
    # db-01: online, CPU 92 %; backup-01: offline
}
_PORT_DIENSTE: Final[dict[int, str]] = {
    22: "SSH", 53: "DNS", 80: "HTTP", 443: "HTTPS",
    3306: "MySQL", 5432: "PostgreSQL", 8080: "HTTP-Alt", 8443: "HTTPS-Alt",
}
# refresh_freigegebene_ports() zieht daraus 3–5 aktuelle Freigaben.
START_NOTIZEN: Final[tuple[str, ...]] = ()
```

Die Aufteilung folgt dem Paketaufbau aus Tag 09. Jede Datei hat eine klar
abgegrenzte Aufgabe:

```text
16_admin_panel.py              # Einstiegspunkt: ft.run(main)
app/
  constants/
    settings.py               # Titel, Grenzwerte und Einstellungen
    theme.py                  # Farben und Statusdarstellung
  models/
    server.py                 # typisierter Serverdatensatz
    status.py                 # gemeinsame Statustypen
  data/
    infrastructure.py         # Server-Inventar
    ports.py                  # Port-Freigabeliste
  services/
    monitoring.py             # Serverstatus auswerten
    analyzer.py               # Hostnamen validieren und suchen
    portcheck.py              # Portnummern validieren und prüfen
    notes.py                  # Notizen validieren und verwalten
  components/
    module_card.py            # gemeinsamer Kartenaufbau
    feedback.py               # einheitliche Rückmeldungen
  views/
    admin_panel.py            # Fenster konfigurieren, Module zusammensetzen
    dashboard.py              # Modul 01
    analyzer.py               # Modul 02
    portcheck.py              # Modul 03
    notes.py                  # Modul 04
```

`constants` und `data` liefern die Einstellungen und Beispieldaten; `models`
definiert die Typen. `services` verarbeitet die Daten ohne Abhängigkeit von
Flet. `views` verbindet Eingabefelder und Buttons mit diesen Funktionen;
`components` enthält wiederverwendbare Darstellung. Die vier vorgegebenen
Modulfunktionen liefern weiterhin jeweils ein `ft.Container`. `main` in
`app/views/admin_panel.py` konfiguriert das Fenster und setzt sie zusammen.
Der gemeinsame Kartenbauer `modul_karte` vermeidet vier Kopien derselben
Gestaltung.

Damit wird die Ein-Datei-Anordnung des Arbeitsblatts auf mehrere Dateien
übertragen: Die fachliche Modularchitektur bleibt erhalten, während die
gewünschte Paketstruktur Konstanten, Typen und Logik getrennt auffindbar macht.
`pyrightconfig.json` aktiviert strikte Typprüfung für den gesamten Ordner.

Die Oberfläche liest Eingaben aus Textfeldern, aber die fachlichen Daten aus
Dictionary bzw. Liste. Eine neue Dashboard-Auswertung verwendet eine Kopie des
Inventars über `get_infrastruktur()`. Jedes Notizmodul erhält mit
`list(START_NOTIZEN)` eine eigene Liste aus der unveränderlichen Vorlage:
keine gemeinsamen Notizen zwischen Sitzungen, keine Speicherung auf Festplatte.
Maximal **20 Notizen mit jeweils 280 Zeichen** sind erlaubt. Leerraum am Rand
wird entfernt; bei einer ungültigen Notiz bleibt die bestehende Liste erhalten.

Hostnamen werden getrimmt und kleingeschrieben. Erlaubt sind einfache Namen bis
63 Zeichen aus ASCII-Buchstaben, Ziffern und inneren Bindestrichen; gesucht wird
ausschließlich im Inventar. Ein Port muss aus 1–5 ASCII-Ziffern bestehen und im
Bereich 1–65535 liegen. Eine gültige, aber nicht gelistete Nummer ist ein
negatives Prüfergebnis, keine Aussage über die Erreichbarkeit eines Dienstes.
Jeder Klick auf **Port prüfen** und jede Bestätigung mit Enter erzeugt zuerst
eine neue Auswahl von 3–5 Ports aus dem hinterlegten Port-Katalog. Die Liste
unter dem Eingabefeld und die Prüfung verwenden dieselbe Auswahl. Auch bei
ungültiger Eingabe wird die Liste erneuert. Zufällig kann dieselbe Auswahl
erneut entstehen.

## Recherche-Antworten

| Control/Eigenschaft | Wozu? |
| --- | --- |
| [`Icon`](https://flet.dev/docs/controls/icon/) | Zeigt ein Symbol; im Panel kennzeichnet es Module und Aktionen zusätzlich zu ihrem Text. |
| [`Divider`](https://flet.dev/docs/controls/divider/) | Horizontale Trennlinie zwischen Bereichen. Die Karten dieses Panels sind bereits durch Abstand und Hintergrund getrennt. |
| [`expand`](https://flet.dev/docs/cookbook/expanding-controls/) | Verteilt freien Platz entlang der Hauptachse von z. B. `Row` oder `Column`; `expand=True` kann ein Eingabefeld neben einem Button verbreitern. |
| [`SnackBar`](https://flet.dev/docs/controls/snackbar/) | Kurze Rückmeldung am Fensterrand, etwa `page.show_dialog(ft.SnackBar(ft.Text("Notiz gespeichert.")))`. Im Panel bleiben Ergebnisse direkt unter den Eingaben sichtbar. |

Zwei weitere Dialoge: Ein [`AlertDialog`](https://flet.dev/docs/controls/alertdialog/)
könnte vor einer folgenreichen Löschaktion eine Entscheidung abfragen; ein
[`DatePicker`](https://flet.dev/docs/controls/datepicker/) könnte das Datum einer
geplanten Wartung auswählen. Das sind Einsatzbeispiele, keine zusätzlichen
Funktionen dieses Panels.

Die gesuchte Button-Eigenschaft heißt
[`disabled`](https://flet.dev/docs/controls/button/). Bei einer späteren
asynchronen Serverabfrage wäre der Ablauf: einen bereits laufenden Aufruf mit
einem `busy`-Guard abweisen, `busy = True` und `button.disabled = True` setzen,
die deaktivierte Ansicht vor dem Warten anzeigen, die Abfrage mit `await`
ausführen und beide Zustände in `finally` zurücksetzen. Dadurch wird auch nach
einem Fehler wieder entsperrt; der Guard erfasst zusätzlich bereits eingereihte
Ereignisse. Die aktuellen lokalen Aktionen sind unmittelbar abgeschlossen und
benötigen keine künstliche Verzögerung. Tatsächlich verwendet wird `disabled`
beim Button **Notizen leeren**, solange die Liste leer ist.

**Korrektur zum Arbeitsauftrag S. 3:** Der Hilfetext verwechselt den Aufbau von
Controls mit Ereignishandlern. `page.add(modul_dashboard())` ist richtig: Die
Funktion wird aufgerufen und liefert ein Control. Bei
`ft.Button(on_click=aktualisieren)` wird dagegen die Funktion **ohne** Klammern
als später auszuführender Handler übergeben. Das Architekturbeispiel auf
derselben Seite und Präsentation S. 5 zeigen `page.add` korrekt.

## Start und Prüfung

Voraussetzung ist Python 3.12 mit Flet 1.0.0 im ausgewählten Interpreter. Die
vorhandene [requirements.txt](../requirements.txt) legt `flet[all]==1.0.0` fest;
dieses Panel benötigt keine weitere Bibliothek.

Vom Repository-Stamm:

```sh
cd Tag_10_GUI_Entwicklung_Planen_Bauen
python --version
python 16_admin_panel.py
```

`python --version` muss Python **3.12.x** ausgeben; in der IDE denselben
Interpreter auswählen.
Alternativ aus demselben Ordner: `flet run 16_admin_panel.py`.
In einer neuen Python-Umgebung können die Projektabhängigkeiten mit
`python -m pip install -r ../requirements.txt` installiert werden.

Für die manuelle Testrunde im laufenden Panel:

| Aktion | Erwartetes Ergebnis |
| --- | --- |
| Dashboard aktualisieren | `web-01` grün, `db-01` mit CPU-Warnung, `backup-01` offline; neue Auswertungszeit |
| Host ` WEB-01 ` suchen | Treffer mit Rolle und IP |
| Leeren Host, `web_01`, unbekannten Host oder 64 Zeichen suchen | Verständlicher roter Fehler; anschließend korrigierbar |
| Port `22` mehrfach prüfen, auch mit Enter | Bei jedem Aufruf wird neu gezogen; grün genau dann, wenn 22 in der danach angezeigten Liste steht, sonst rot |
| Port `443`, `8080`, `1`, `65535` prüfen | Ergebnis entspricht jeweils der neu angezeigten Auswahl; 1 und 65535 sind gültig, aber nicht im Port-Katalog |
| Port leer, `ssh`, `-1`, `22.0`, `0`, `65536`, `４４３` oder sehr lange Zahl | Verständlicher Fehler, keine Änderung am Inventar |
| Notiz mit Umlauten/Zeilenumbruch speichern | Nummerierter Eintrag; Shift+Enter fügt eine neue Zeile ein |
| Leere Notiz, 281 Zeichen oder 21. Notiz speichern | Fehlermeldung, bestehende Notizen bleiben erhalten |
| Notizen leeren; neues Fenster/neue Sitzung öffnen | Leere Liste, deaktivierter Leeren-Button; kein Übernehmen alter Notizen |
| Fenster schmal/klein ziehen; Fehler danach korrigieren | Bedienelemente erreichbar, Scrollen möglich, Fehlermeldung nach Erfolg gelöscht |

## Kursabgabe

Abnahme durch den Kursleiter und Einfügen von Screenshots in das persönliche
Doku-Dokument sind menschliche Kursschritte (Arbeitsauftrag S. 2, 5;
Präsentation S. 4, 8). Sie werden hier nicht als durchgeführt ausgewiesen.
Für die Abgabe noch selbst erstellen/einfügen: Skizze mit Datenmodell, laufendes
Panel mit allen Modulen sowie ein Modul mit gültiger und ungültiger Eingabe.
Als Dokumentüberschrift ist „GUI-Entwicklung II: Planen & Bauen — Admin-Panel“
vorgegeben; Funktionsliste und Recherche-Antworten stehen oben bereit.

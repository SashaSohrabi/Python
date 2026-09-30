# Skriptname: aufgabe_4_lueckencode.py
# Autor: Sasha Sohrabi
# Datum: 29.09.2026
# Zweck: Den unabhängigen Lückencode aus Aufgabe 4 vervollständigen.


class Server:
    def __init__(self, name: str, rolle: str) -> None:
        self.name = name
        self.rolle = rolle

    def diagnose(self) -> str:
        return f"{self.name}: läuft."


class BackupServer(Server):
    def __init__(self, name: str, cpu_load: int, laufzeit_seit: str) -> None:
        super().__init__(name, "Backup") 
        self._laufzeit_seit = laufzeit_seit

    @property  
    def laufzeit_seit(self) -> str:
        return self._laufzeit_seit

    def diagnose(self) -> str: 
        return super().diagnose() + " (gut, dass du fragst …)"


if __name__ == "__main__":
    backup = BackupServer("backup-01", 3, "2014")
    print(backup.diagnose())  
    print(
        "Ohne die überschreibende Methode diagnose() würde der Aufruf weiterhin "
        "funktionieren: Python würde die geerbte Version aus Server verwenden."
    )

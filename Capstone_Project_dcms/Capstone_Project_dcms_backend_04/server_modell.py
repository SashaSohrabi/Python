class Server:
    def __init__(self, name: str, ip: str, os: str) -> None:
        self.name = name
        self.ip = ip
        self.os = os
        self.status = "offline"

    def ping(self) -> bool:
        return self.status == "online"

    def status_wechseln(self) -> None:
        if self.status == "offline":
            self.status = "online"
        else:
            self.status = "offline"


class Webserver(Server):
    def __init__(
        self,
        name: str,
        ip: str,
        os: str,
        domain: str,
        ssl_aktiv: bool,
    ) -> None:
        super().__init__(name, ip, os)
        self.domain = domain
        self.ssl_aktiv = ssl_aktiv


class DatenbankServer(Server):
    def __init__(
        self,
        name: str,
        ip: str,
        os: str,
        db_typ: str,
        port: int,
    ) -> None:
        super().__init__(name, ip, os)
        self.db_typ = db_typ
        self.port = port

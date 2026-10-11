CPU_WARNING_THRESHOLD = 80
BACKUP_WARNING_THRESHOLD = 95
LEGACY_WARNING_THRESHOLD = 60
WEB_WARNING_THRESHOLD = 60


class Server:
    def __init__(
        self, name: str, ip: str, role: str, cpu_load: int, status: str
    ) -> None:
        self._name = name
        self._ip = ip
        self._role = role
        self.cpu_load = cpu_load
        self.status = status

    @property
    def name(self) -> str:
        return self._name

    @property
    def ip(self) -> str:
        return self._ip

    @property
    def role(self) -> str:
        return self._role

    @property
    def cpu_load(self) -> int:
        return self._cpu_load

    @cpu_load.setter
    def cpu_load(self, value: int) -> None:
        if type(value) is not int:
            raise TypeError("cpu_load must be an integer")
        if not 0 <= value <= 100:
            raise ValueError("cpu_load must be between 0 and 100")
        self._cpu_load = value

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str) -> None:
        if value not in ("online", "offline"):
            raise ValueError("status must be 'online' or 'offline'")
        self._status = value

    def is_offline(self) -> bool:
        return self.status == "offline"

    def is_critical(self) -> bool:
        return not self.is_offline() and self.cpu_load > CPU_WARNING_THRESHOLD

    def __str__(self) -> str:
        return f"{self.name} ({self.role}) - CPU {self.cpu_load}% - {self.status}"


class BackupServer(Server):
    def __init__(
        self, name: str, ip: str, cpu_load: int, status: str, last_backup: str
    ) -> None:
        super().__init__(name, ip, "Backup", cpu_load, status)
        self._last_backup = last_backup

    @property
    def last_backup(self) -> str:
        return self._last_backup

    def is_critical(self) -> bool:
        return self.is_offline() or self.cpu_load > BACKUP_WARNING_THRESHOLD

    def __str__(self) -> str:
        return f"{super().__str__()} (last backup: {self.last_backup})"


class LegacyServer(Server):
    def __init__(
        self, name: str, ip: str, cpu_load: int, status: str, patch_level: str
    ) -> None:
        super().__init__(name, ip, "Legacy", cpu_load, status)
        self._patch_level = patch_level

    @property
    def patch_level(self) -> str:
        return self._patch_level

    def is_critical(self) -> bool:
        return not self.is_offline() and self.cpu_load > LEGACY_WARNING_THRESHOLD

    def __str__(self) -> str:
        return f"{super().__str__()} (patch level: {self.patch_level})"


class WebServer(Server):
    def __init__(
        self, name: str, ip: str, role: str, cpu_load: int, status: str, port: int
    ) -> None:
        super().__init__(name, ip, role, cpu_load, status)
        self.port = port

    def is_critical(self) -> bool:
        return self.cpu_load > WEB_WARNING_THRESHOLD


class MailServer(Server):
    def __init__(
        self, name: str, ip: str, cpu_load: int, status: str, since: str
    ) -> None:
        super().__init__(name, ip, "Mail", cpu_load, status)
        self.since = since


class Ticket:
    def __init__(self, title: str, status: str, priority: int) -> None:
        self.title = title
        self.status = status
        self.priority = priority

    def __str__(self) -> str:
        return f"[{self.priority}] {self.title} ({self.status})"


class UrgentTicket(Ticket):
    def __init__(self, title: str, status: str, priority: int, sla: int) -> None:
        super().__init__(title, status, priority)
        self.sla = sla

    def __str__(self) -> str:
        return f"{super().__str__()} - SLA {self.sla} h"


def print_server_table(servers: list[Server]) -> None:
    print(
        f"{'Name':<12} {'Class':<15} {'Role':<12} "
        f"{'CPU':>5} {'Status':<9} {'Critical':<8}"
    )
    for server in servers:
        print(
            f"{server.name:<12} {type(server).__name__:<15} {server.role:<12} "
            f"{server.cpu_load:>4}% {server.status:<9} {server.is_critical()!s:<8}"
        )
    critical_count = sum(server.is_critical() for server in servers)
    class_count = len({type(server) for server in servers})
    print(
        f"\n{len(servers)} objects, {class_count} classes, "
        f"{critical_count} critical servers"
    )


def print_instance_report(web: object, backup: object, legacy: object) -> None:
    print(f"\nisinstance(backup, BackupServer): {isinstance(backup, BackupServer)}")
    print(f"isinstance(backup, Server): {isinstance(backup, Server)}")
    print(f"isinstance(web, BackupServer): {isinstance(web, BackupServer)}")
    print(f"isinstance(legacy, LegacyServer): {isinstance(legacy, LegacyServer)}")
    print(f"type(backup) is Server: {type(backup) is Server}")

    print("\nResolved methods:")
    for server in (web, backup, legacy):
        if not isinstance(server, Server):
            continue
        print(
            f"{server.name}: {server.is_critical.__qualname__} "
            f"-> {server.is_critical()}"
        )
        print(f"{server.name}: {server.__str__.__qualname__} -> {server}")


def print_super_report(backup: BackupServer) -> None:
    print(f'super().__init__(name, ip, "{backup.role}", cpu_load, status)')
    print(f"backup.role: {backup.role}")
    print("BackupServer supplies the role; its caller does not pass it.")
    print("Server.__init__ initializes the inherited attributes on the same object.")
    print(f"Base representation: {Server.__str__(backup)}")
    print(f"Extended with super().__str__(): {backup}")


def print_self_report(backup: BackupServer) -> None:
    inheritance_chain = " -> ".join(
        server_class.__name__ for server_class in type(backup).__mro__
    )
    print(f"Method resolution order: {inheritance_chain}")
    print(f"self refers to the same {type(backup).__name__} instance in both classes.")
    print("super() starts after BackupServer in this order and finds Server next.")
    print("Server.__init__ sets self.status, whose setter creates self._status.")


def is_server(value: object) -> bool:
    return isinstance(value, Server)


def run_afternoon_assignment() -> None:
    web = WebServer("web-02", "192.168.1.11", "Frontend", 61, "online", 8080)
    regular = Server("server-02", "192.168.1.12", "Frontend", 61, "online")
    backup = BackupServer("backup-02", "192.168.1.31", 5, "online", "2026-10-06 03:00")
    mail = MailServer("mail-01", "192.168.1.40", 30, "online", "2026-09-12")

    print("\nAFTERNOON PART 1: WebServer inherits and overrides\n")
    print_server_table([regular, web])
    print(f"web.port: {web.port}")
    print(f"isinstance(web, Server): {is_server(web)}")
    print(f"Inherited __str__(): {web}")

    print("\nAFTERNOON PART 2: MailServer uses the base constructor\n")
    print(f"mail.role: {mail.role}")
    print(f"mail.since: {mail.since}")
    print(mail)
    print(
        "Copying the name and CPU assignments skips Server.__init__(), "
        "leaving the role uninitialized and bypassing the CPU setter."
    )
    print("super().__init__() initializes all inherited fields and runs the setters.")

    print("\nAFTERNOON PART 3: One fleet, one loop\n")
    fleet: list[Server] = [web, backup, mail]
    for server in fleet:
        print(server.name, type(server).__name__, server.is_critical())

    print("\nAFTERNOON PART 4: Ticket inheritance and text representation\n")
    tickets: list[Ticket] = [
        Ticket("Printer issue", "open", 2),
        UrgentTicket("Mail server unavailable", "open", 1, 4),
    ]
    for ticket in tickets:
        print(ticket)
    print(
        "UrgentTicket reuses Ticket.__str__() and appends its SLA, "
        "so the common text format is defined once and inherited changes carry through."
    )

    print("\nBONUS: The inherited CPU setter still validates WebServer\n")
    try:
        web.cpu_load = 120
    except ValueError as error:
        print(f"web.cpu_load = 120 -> {type(error).__name__}: {error}")
    print(f"web.cpu_load remains: {web.cpu_load}")
    print(
        "WebServer inherits the cpu_load property; assigning to it runs "
        "Server's setter even though is_critical() is overridden."
    )


def main() -> None:
    web = Server("web-01", "192.168.1.10", "Frontend", 45, "online")
    backup = BackupServer("backup-01", "192.168.1.30", 5, "offline", "2026-09-24 03:00")
    legacy = LegacyServer("alt-vm-1", "192.168.1.99", 71, "online", "2023-11")
    database = Server("db-01", "192.168.1.20", "Database", 92, "online")
    servers: list[Server] = [web, backup, legacy, database]

    print("PART 1: Classes, objects, properties and overridden methods\n")
    print_server_table(servers)
    print_instance_report(web, backup, legacy)

    print("\nPART 2: The role supplied by super()\n")
    print_super_report(backup)

    print("\nPART 3: self and the method resolution order\n")
    print_self_report(backup)

    run_afternoon_assignment()


if __name__ == "__main__":
    main()

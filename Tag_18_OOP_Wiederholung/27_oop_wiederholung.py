CPU_WARNING_THRESHOLD = 80
BACKUP_WARNING_THRESHOLD = 95
LEGACY_WARNING_THRESHOLD = 60


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
    print(f"\n{len(servers)} objects, 3 classes, {critical_count} critical servers")


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


if __name__ == "__main__":
    main()

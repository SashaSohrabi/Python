hostnamen: list[str] = []
hostnamen.append("Router-01")
hostnamen.append("Switch-Core")
hostnamen.append("Firewall-Extern")
anzahl = len(hostnamen)

print(f"Es wurden {anzahl} Systeme registriert:")

for host in hostnamen:
    print(f"-> Führe Ping aus für: {host}")

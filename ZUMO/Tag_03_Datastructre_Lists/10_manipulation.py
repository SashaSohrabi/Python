"""
Skript: Warteschlangen-Manipulation
Autor: Sasha Sohrabi
Datum: 08.09.2026
Zweck: Aufgaben-Warteschlange bearbeiten und sortieren.
"""

task_queue = ["Updates installieren", "Backups prüfen"]

task_queue.append("Logs archivieren")
print(f"Task-Warteschlange: {task_queue}")

task_queue.insert(0, "Server-Neustart")
print(f"Task-Warteschlange: {task_queue}")

item = task_queue.pop(0)
print(f"Verarbeiteter Eintrag: {item}")
print(f"Task-Warteschlange: {task_queue}")

task_queue.sort()
print(f"Sortierte Task-Warteschlange: {task_queue}")


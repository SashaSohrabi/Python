import subprocess

while True:
    befehl = input("Drücken Sie einen Befehl... ")
    if befehl == "clear":
        subprocess.run("cls", shell=True)
    elif befehl == "exit":
        break
    else:
        print(f"Der Befehl '{befehl}' ist nicht bekannt.")

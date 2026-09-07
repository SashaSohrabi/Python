import os

while True:
    befehl = input("Drücken Sie einen Befehl... ")
    if befehl == "clear":
        os.system("cls")
    elif befehl == "exit":
        break
    else:
        print(f"Der Befehl '{befehl}' ist nicht bekannt.")

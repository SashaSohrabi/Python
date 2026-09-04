print("--- Capacity Check ---")
initialen = input("Please enter your initials: ")
server_anzahl_text = input("How many servers would you like to administer today?")
server_anzahl = int(server_anzahl_text)

if server_anzahl > 10: print(f"Warning to {initialen}: That is too much for one day. Do not overload yourself!")
elif server_anzahl == 0: print(f"Note to {initialen}: You do need to do at least a little work today.")
else: print(f"Approved! {initialen} is administering {server_anzahl} servers today. Good luck!")
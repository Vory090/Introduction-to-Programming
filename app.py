jmeno = input("Zadej svoje jméno: ")

print("Vyber možnost:")
print("1 - formálně")
print("2 - neformálně")
vyber = input("Zadej 1 nebo 2: ")

if vyber == "1" or vyber.lower() == "formálně":
    print(f"Dobrý den, {jmeno}!")
elif vyber == "2" or vyber.lower() == "neformálně":
    print(f"Ahoj, {jmeno}!")
else:
    print("Neplatná volba. Zadej prosím 1 nebo 2.")

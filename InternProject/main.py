import random

pferde = {
    1: 45, # %chance of winning
    2: 30, # %chance of winning
    3: 20, # %chance of winning
    4: 5   # %chance of winning
}

print("Willkommen beim Pferderennen!")
print("Verfügbare Pferde und deren Gewinnchancen: ")
for pferd, chance in pferde.items():
    multiplier = 100 / chance
    print(f"Pferde {pferd}: {chance}% chance - Payout : x{multiplier:.2f}")


try:
    bet = int(input("\nGeben Sie die Anzahl der Pferde ein, auf die Sie wetten möchten: "))
    if bet not in pferde.keys():
        print("Ungültige Pferdenummer! Bitte starten Sie das Spiel neu.")
    else:
        stake = float(input("Geben Sie Ihren Einsatzbetrag ein: €"))
        if stake <= 0:
            print("Ungültige Pferdenummer! Bitte starten Sie das Spiel neu.")
        else:
            gewinnendes_Pferd = random.choices(list(pferde.keys()), weights=list(pferde.values()))[0]

            print(f"\nDas Rennen ist vorbei! Das Siegerpferd ist: {gewinnendes_Pferd}")
            if bet == gewinnendes_Pferd:
                multiplier = 100 / pferde[bet]
                gewinn = stake * multiplier
                print(f"Glückwunsch! Du hast die Wette gewonnen! Ihre Auszahlung beträgt: €{gewinn:.2f}")
            else:
                print("Entschuldigung, du hast verloren. Viel Glück beim nächsten Mal!")
except ValueError:
    print("Ungültige Eingabe! Bitte geben Sie eine gültige Nummer ein.")
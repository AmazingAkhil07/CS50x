while True:
    try:
        change = float(input("Change owed: "))
        if change >= 0:
            break
    except ValueError:
        pass

# Convert dollars to cents, rounding to avoid floating-point issues
cents = round(change * 100)

coins = 0

# Quarters
coins += cents // 25
cents %= 25

# Dimes
coins += cents // 10
cents %= 10

# Nickels
coins += cents // 5
cents %= 5

# Pennies
coins += cents

print(coins)

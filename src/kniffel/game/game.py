from kniffel.game.dice import Dice, DiceCup

cup = DiceCup()

#print(cup)

print(cup.values())

cup.roll_all()

print("rolled")

print(cup.values())
print(cup.rolls_left())
print(cup.get_diceList())

for d in cup.get_diceList():
    print(d.value)
from kniffel.game.dice import Dice, DiceCup

cup = DiceCup()

#print(cup)

print(f"Values: {cup.values()}\n")


for d in cup.get_diceList():
    print(f"D Value: {d.value} ")
    print(f"ID: {d.dice_id} \n")


cup.roll_all()

print("rolled\n")
cup.sort_dice()

print(f"Velues after rolling: {cup.values()}\n")
print(f"rolles left: {cup.rolls_left()}\n")
#print(cup.get_diceList())

for d in cup.get_diceList():
    print(f"D Value: {d.value} ")
    print(f"ID: {d.dice_id} \n")

cup.roll_all()
cup.sort_dice()

print("rolled")

print(f"Velues after rolling: {cup.values()}")
print(f"rolles left: {cup.rolls_left()}")

for d in cup.get_diceList():
    print(f"D Value: {d.value} ")
    print(f"ID: {d.dice_id} \n")

from app import Dice_Button_List
from kniffel.game.dice import Dice, DiceCup    

DICE_PER_CUP = 5

'''Placeholder atm for sorting Algorythm in GUI'''
def sort_dice(self):
    for i in range(Dice_Button_List):
        for j in range(DICE_PER_CUP-1):
            if self._dice[j].value > self._dice[j+1].value:
                self._dice[j], self._dice[j+1] = self._dice[j+1], self._dice[j]
''' ^ soll nach Value sortieren'''

if __name__ == "__main__":
    pass
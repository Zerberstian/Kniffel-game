"""Würfel-Logik für Kniffel: einzelner Würfel und Würfelbecher."""
from __future__ import annotations

import random
from typing import List

MIN_VALUE = 1
MAX_VALUE = 6
DICE_PER_CUP = 5
ROLLS_PER_TURN = 3


class Dice:
    """Ein einzelner Würfel mit Wert und Halten-Zustand."""

    def __init__(self, dice_id) -> None:
        self._value: int = MIN_VALUE
        self._held: bool = False
        self.id = dice_id

    @property
    def value(self) -> int:
        return self._value

    @property
    def held(self) -> bool:
        return self._held

    def roll(self) -> None:
        self._value = random.randint(MIN_VALUE, MAX_VALUE)

    def hold(self) -> None:
        self._held = True

    def release(self) -> None:
        self._held = False


class DiceCup:
    """Becher mit 5 Würfeln, verwaltet die Würfe pro Zug."""

    def __init__(self) -> None:
        self._dice: List[Dice] = [Dice() for _ in range(DICE_PER_CUP)]
        self._rolls_left: int = ROLLS_PER_TURN

    #@property
    def rolls_left(self) -> int:
        return self._rolls_left

    def roll_all(self) -> None:
        self._consume_roll()
        for die in self._dice:
            die.roll()

    def roll_unheld(self) -> None:
        self._consume_roll()
        for die in self._dice:
            if not die.held:
                die.roll()

    def reset(self) -> None:
        for die in self._dice:
            die.release()
        self._rolls_left = ROLLS_PER_TURN

    def values(self) -> List[int]:
        return [die.value for die in self._dice]

    def _consume_roll(self) -> None:
        if self._rolls_left <= 0:
            raise RuntimeError("Keine Würfe mehr in diesem Zug übrig.")
        self._rolls_left -= 1

    def get_diceList(self) ->  List[Dice]:
        return self._dice
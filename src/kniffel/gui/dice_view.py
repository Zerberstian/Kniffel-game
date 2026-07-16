import tkinter as tk
from typing import List

from ..game.dice import Dice


class DiceView:
    """Zeigt die Würfel sortiert nach Wert an; die dice_id bleibt am Widget erhalten."""

    def __init__(self, master: tk.Widget) -> None:
        self.master = master
        self._labels: List[tk.Label] = []

    def render(self, dice: List[Dice]) -> None:
        for label in self._labels:
            label.destroy()
        self._labels = []

        for die in sorted(dice, key=lambda d: d.value):
            text = str(die.value) + (" *" if die.held else "")
            label = tk.Label(self.master, text=text)
            label.dice_id = die.dice_id
            label.pack(side=tk.LEFT)
            self._labels.append(label)

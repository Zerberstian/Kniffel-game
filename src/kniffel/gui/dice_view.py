import tkinter as tk
from typing import Callable, List

from ..game.dice import Dice


class DiceView:
    """Zeigt die Würfel sortiert nach Wert an; die dice_id bleibt am Widget erhalten."""

    def __init__(self, master: tk.Widget, on_dice_clicked: Callable[[int], None]) -> None:
        self.master = master
        self._on_dice_clicked = on_dice_clicked
        self._labels: List[tk.Label] = []
        self._enabled = True

    def set_enabled(self, enabled: bool) -> None:
        self._enabled = enabled

    def render(self, dice: List[Dice]) -> None:
        for label in self._labels:
            label.destroy()
        self._labels = []

        for die in sorted(dice, key=lambda d: d.value):
            label_text = str(die.value) + (" *" if die.held else "")
            label = tk.Label(self.master, text=label_text)
            label.dice_id = die.dice_id
            label.bind("<Button-1>", lambda event, dice_id=die.dice_id: self._handle_click(dice_id))
            label.pack(side=tk.LEFT)
            self._labels.append(label)

    def _handle_click(self, dice_id: int) -> None:
        if self._enabled:
            self._on_dice_clicked(dice_id)

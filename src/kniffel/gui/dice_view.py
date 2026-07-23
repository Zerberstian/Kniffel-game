import tkinter as tk
from typing import Callable, List

from ..game.dice import Dice

DICE_BG = "#ffffff"
LOCK_BG = "#f4c95d"
DICE_FONT = ("Segoe UI", 28, "bold")
CAPTION_FONT = ("Segoe UI", 11)
PLACEHOLDER_TEXT = "-"
ROW_HEIGHT = 90


class DiceView:
    """Zeigt Würfel in zwei Reihen: gehaltene Würfel oben (Lock), aktive Würfel unten (Play)."""

    def __init__(self, master: tk.Widget, on_dice_clicked: Callable[[int], None]) -> None:
        self.master = master
        self._on_dice_clicked = on_dice_clicked
        self._held_labels: List[tk.Label] = []
        self._active_labels: List[tk.Label] = []
        self._enabled = True

        tk.Label(master, text="Gehalten:", font=CAPTION_FONT, bg=LOCK_BG).pack(side=tk.TOP, fill=tk.X)
        self._lock_row = tk.Frame(master, bg=LOCK_BG, height=ROW_HEIGHT)
        self._lock_row.pack(side=tk.TOP, fill=tk.X)
        self._lock_row.pack_propagate(False)

        tk.Label(master, text="Im Spiel:", font=CAPTION_FONT, bg=DICE_BG).pack(side=tk.TOP, fill=tk.X)
        self._play_row = tk.Frame(master, bg=DICE_BG, height=ROW_HEIGHT)
        self._play_row.pack(side=tk.TOP, fill=tk.X, expand=True)
        self._play_row.pack_propagate(False)

    def set_enabled(self, enabled: bool) -> None:
        self._enabled = enabled

    def render(self, dice: List[Dice], has_rolled: bool = True) -> None:
        for label in self._held_labels + self._active_labels:
            label.destroy()

        held = sorted([d for d in dice if d.held], key=lambda d: d.value)
        active = sorted([d for d in dice if not d.held], key=lambda d: d.value)
        self._held_labels = [self._make_label(self._lock_row, die, has_rolled) for die in held]
        self._active_labels = [self._make_label(self._play_row, die, has_rolled) for die in active]

    def _make_label(self, row: tk.Frame, die: Dice, has_rolled: bool) -> tk.Label:
        text = str(die.value) if has_rolled else PLACEHOLDER_TEXT
        label = tk.Label(
            row,
            text=text,
            font=DICE_FONT,
            bg=row["bg"],
            relief=tk.RAISED,
            borderwidth=3,
            width=2,
            height=1,
            cursor="hand2",
        )
        label.dice_id = die.dice_id
        label.bind("<Button-1>", lambda event, dice_id=die.dice_id: self._handle_click(dice_id))
        label.pack(side=tk.LEFT, padx=8, pady=8, ipadx=6, ipady=4)
        return label

    def _handle_click(self, dice_id: int) -> None:
        if self._enabled:
            self._on_dice_clicked(dice_id)

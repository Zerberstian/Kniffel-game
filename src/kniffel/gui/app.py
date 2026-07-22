"""Baut das Fenster auf und verbindet Game/GameConnector mit DiceView/ScorecardView."""
import tkinter as tk
from pathlib import Path
from typing import List, Optional

from ..connector.game_connector import GameConnector
from ..game.category import (
    Chance,
    FourOfAKind,
    FullHouse,
    Kniffel,
    LargeStraight,
    NumberCategory,
    ScoreCategory,
    SmallStraight,
    ThreeOfAKind,
)
from ..game.game import Game
from .dice_view import DiceView
from .Scorecard_view import (
    DICE_BG,
    FONTSIZE,
    FONTSIZESMOL,
    FONTSTYLE,
    NUMBER_OF_CATEGORIES,
    ScoreFrame,
    ScorecardView,
)

RULES_PATH = Path(__file__).parent / "regeln.txt"


def build_categories() -> List[ScoreCategory]:
    return [
        NumberCategory("Einer", 1),
        NumberCategory("Zweier", 2),
        NumberCategory("Dreier", 3),
        NumberCategory("Vierer", 4),
        NumberCategory("Fünfer", 5),
        NumberCategory("Sechser", 6),
        ThreeOfAKind("Dreierpasch"),
        FourOfAKind("Viererpasch"),
        FullHouse("Full House"),
        SmallStraight("Kleine Straße"),
        LargeStraight("Große Straße"),
        Kniffel("Kniffel"),
        Chance("Chance"),
    ]


class App:
    """Erzeugt Fenster + Widgets und verknüpft sie über GameConnector mit Game."""

    def __init__(self, player_names: List[str], master: Optional[tk.Misc] = None) -> None:
        categories = build_categories()
        self._game = Game(player_names, categories)

        '''master erlaubt Tests, sich einen Tk-Root zu teilen statt für jeden Fall einen neuen zu erzeugen'''
        self.root = master if master is not None else tk.Tk()
        self.root.title("Kniffel Game")
        self.root.maxsize(width=1920, height=1080)
        self.root.minsize(width=900, height=600)
        self.root.geometry("1600x900")
        self.root.configure(bg="green")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=2)
        self.root.grid_rowconfigure(1, weight=2)

        scorecard_area = tk.Frame(self.root, bg="lightgray")
        scorecard_area.grid(row=0, column=1, rowspan=2, sticky="nsew")

        dice_playarea = tk.Frame(self.root, bg="#499240")
        dice_playarea.grid(column=0, row=0, sticky="nsew")
        dice_playarea.grid_rowconfigure(0, minsize=200)
        for column in range(5):
            dice_playarea.grid_columnconfigure(column, weight=1)

        '''DiceView packt seine Labels; braucht daher einen eigenen Frame statt Dice_Playarea selbst '''
        dice_row = tk.Frame(dice_playarea, bg=DICE_BG)
        dice_row.grid(column=0, row=0, columnspan=5, sticky="nsew")

        reroll_button = tk.Button(dice_playarea, bg=DICE_BG, text="roll", font=(FONTSTYLE, FONTSIZE))
        reroll_button.grid(column=5, row=1, ipadx=10, ipady=10)

        status_label = tk.Label(dice_playarea, bg=DICE_BG, font=(FONTSTYLE, FONTSIZE), text="")
        status_label.grid(column=0, row=1, columnspan=5, sticky="nsew")

        rule_text_widget = tk.Text(self.root, font=(FONTSTYLE, FONTSIZESMOL))
        rule_text_widget.grid(column=0, row=1, sticky="nsew")
        rule_text_widget.insert(tk.END, RULES_PATH.read_text(encoding="utf-8"))

        score_frames = [ScoreFrame(scorecard_area, i) for i in range(NUMBER_OF_CATEGORIES)]
        for frame in score_frames:
            frame.pack(side="top", fill="both", expand=True)
            frame.configure(bg="#c46464")

        connector = GameConnector(self._game, self)
        self.dice_view = DiceView(dice_row, on_dice_clicked=connector.on_hold_toggle)
        self.scorecard_view = ScorecardView(score_frames, categories, on_category_chosen=connector.on_category_chosen)
        self.reroll_button = reroll_button
        self.status_label = status_label
        reroll_button.configure(command=connector.on_roll)

        connector.refresh_view()

    def show_winner(self, name: str, score: int) -> None:
        self.status_label.configure(text=f"{name} gewinnt mit {score} Punkten!")
        self.reroll_button.configure(state=tk.DISABLED)
        self.dice_view.set_enabled(False)
        self.scorecard_view.set_enabled(False)

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    App(["Spieler 1", "Spieler 2"]).run()

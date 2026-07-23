"""Baut das Fenster auf und verbindet Game/GameConnector mit DiceView/ScorecardView."""
import tkinter as tk
from pathlib import Path
from tkinter import messagebox
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
from ..game.dice import ROLLS_PER_TURN
from ..game.game import Game
from .dice_view import DiceView
from .Scorecard_view import (
    DICE_BG,
    LOWER_BONUS_INDEX,
    NUMBER_OF_CATEGORIES,
    TOTAL_INDEX,
    UPPER_BONUS_INDEX,
    ScoreFrame,
    ScorecardView,
)

RULES_PATH = Path(__file__).parent / "regeln.txt"

'''Eigene Schrift fürs Würfel-/Status-Areal statt der Scorecard-Schrift'''
PLAYAREA_FONT = ("Segoe UI", 16, "bold")
ACCENT_BG = "#f4c95d"
ACCENT_ACTIVE_BG = "#e0b64f"

'''Eine Farbe je Spieler (zyklisch per Modulo bei mehr als 2 Spielern), nur der Würfelbereich wechselt die Farbe'''
PLAYER_COLORS = ("#2f6b3a", "#2f4d78")
'''Auffällige Warnfarbe, wenn die Würfe aufgebraucht sind und eine Kategorie gewählt werden muss'''
TURN_DONE_BG = "#b03a2e"

RULES_HEADING_FONT = ("Segoe UI", 15, "bold")
RULES_SUBHEADING_FONT = ("Segoe UI", 12, "bold")
RULES_BODY_FONT = ("Segoe UI", 12)
_RULES_SECTION_HEADINGS = {"Ziel:", "Spielablauf:", "Spielplan:", "Bonus:", "Spielende:"}
_RULES_CATEGORY_NAMES = {
    "Einer", "Zweier", "Dreier", "Vierer", "Fünfer", "Sechser",
    "Dreierpasch", "Viererpasch", "Full House", "Kleine Straße",
    "Große Straße", "Kniffel", "Chance",
}


def _insert_formatted_rules(widget: tk.Text, text: str) -> None:
    """Formatiert regeln.txt lesbarer: fette Überschriften/Kategorienamen statt einem Fließtextblock."""
    widget.tag_configure("heading", font=RULES_HEADING_FONT, spacing1=14, spacing3=6)
    widget.tag_configure("subheading", font=RULES_SUBHEADING_FONT, spacing1=8)
    widget.tag_configure("body", font=RULES_BODY_FONT, spacing3=4)

    for line in text.splitlines():
        if line in _RULES_SECTION_HEADINGS:
            tag = "heading"
        elif line in _RULES_CATEGORY_NAMES:
            tag = "subheading"
        else:
            tag = "body"
        widget.insert(tk.END, line + "\n", tag)


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
        self.root.configure(bg="#1f4d2b")
        self.root.grid_columnconfigure(0, weight=2)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=2)
        self.root.grid_rowconfigure(1, weight=2)

        scorecard_area = tk.Frame(self.root, bg="#eef1f5")
        scorecard_area.grid(row=0, column=1, rowspan=2, sticky="nsew")

        dice_playarea = tk.Frame(self.root, bg="#2f6b3a")
        dice_playarea.grid(column=0, row=0, sticky="nsew")
        dice_playarea.grid_rowconfigure(0, minsize=260)
        dice_playarea.grid_rowconfigure(1, weight=0)
        dice_playarea.grid_columnconfigure(0, weight=1)
        dice_playarea.grid_columnconfigure(1, weight=0)

        '''DiceView baut seine zwei Reihen (gehalten/aktiv) selbst innerhalb von dice_area auf'''
        dice_area = tk.Frame(dice_playarea, bg=DICE_BG)
        dice_area.grid(column=0, row=0, sticky="nsew", padx=12, pady=12)

        reroll_button = tk.Button(
            dice_playarea,
            bg=ACCENT_BG,
            activebackground=ACCENT_ACTIVE_BG,
            fg="#1f4d2b",
            text="Würfeln",
            font=PLAYAREA_FONT,
            relief=tk.RAISED,
            borderwidth=3,
            cursor="hand2",
        )
        reroll_button.grid(column=1, row=0, sticky="ns", padx=(0, 12), pady=12, ipadx=14, ipady=14)

        status_label = tk.Label(dice_playarea, bg="#2f6b3a", fg="white", font=PLAYAREA_FONT, text="")
        status_label.grid(column=0, row=1, columnspan=2, sticky="nsew")

        rule_text_widget = tk.Text(self.root, font=RULES_BODY_FONT, padx=16, pady=10, wrap=tk.WORD)
        rule_text_widget.grid(column=0, row=1, sticky="nsew")
        _insert_formatted_rules(rule_text_widget, RULES_PATH.read_text(encoding="utf-8"))
        rule_text_widget.configure(state=tk.DISABLED)

        '''Bonus-/Ergebnis-Zeilen (berechnet statt anklickbar) etwas stärker abgesetzt, Kategorie-Zeilen abwechselnd gestreift'''
        VIRTUAL_ROW_BG = "#c9d6e8"
        ROW_BG = ("#dfe7f2", "#eef1f5")
        score_frames = [
            ScoreFrame(
                scorecard_area,
                i,
                bg=VIRTUAL_ROW_BG if i in (UPPER_BONUS_INDEX, LOWER_BONUS_INDEX, TOTAL_INDEX) else ROW_BG[i % 2],
            )
            for i in range(NUMBER_OF_CATEGORIES)
        ]
        for frame in score_frames:
            frame.pack(side="top", fill="both", expand=True)

        connector = GameConnector(self._game, self)
        self.dice_view = DiceView(dice_area, on_dice_clicked=connector.on_hold_toggle)
        self.scorecard_view = ScorecardView(score_frames, categories, on_category_chosen=connector.on_category_chosen)
        self.reroll_button = reroll_button
        self.status_label = status_label
        self.dice_playarea = dice_playarea
        self.rule_text_widget = rule_text_widget
        self._current_player_bg = PLAYER_COLORS[0]
        reroll_button.configure(command=connector.on_roll)

        connector.refresh_view()

    def set_rolls_remaining(self, rolls_left: int) -> None:
        if rolls_left > 0:
            self.reroll_button.configure(state=tk.NORMAL, text=f"{rolls_left}x Würfeln")
        else:
            self.reroll_button.configure(state=tk.DISABLED, text="Kategorie wählen")

    def set_active_player_color(self, index: int) -> None:
        self._current_player_bg = PLAYER_COLORS[index % len(PLAYER_COLORS)]
        self.dice_playarea.configure(bg=self._current_player_bg)

    def set_turn_status(self, player_name: str, rolls_left: int) -> None:
        thrown = ROLLS_PER_TURN - rolls_left
        if rolls_left == 0:
            text = f"{player_name} - bitte Kategorie wählen!"
            self.status_label.configure(text=text, bg=TURN_DONE_BG)
        elif thrown == 0:
            text = f"{player_name} ist am Zug - bereit zum Würfeln"
            self.status_label.configure(text=text, bg=self._current_player_bg)
        else:
            text = f"{player_name} ist am Zug - Wurf {thrown} von {ROLLS_PER_TURN}"
            self.status_label.configure(text=text, bg=self._current_player_bg)

    def confirm_zero_score(self, category_name: str) -> bool:
        return messagebox.askyesno("Bestätigen", f"Wirklich 0 Punkte bei '{category_name}' eintragen?")

    def show_winner(self, name: str, score: int) -> None:
        self.status_label.configure(text=f"{name} gewinnt mit {score} Punkten!")
        self.reroll_button.configure(state=tk.DISABLED)
        self.dice_view.set_enabled(False)
        self.scorecard_view.set_enabled(False)

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    App(["Spieler 1", "Spieler 2"]).run()

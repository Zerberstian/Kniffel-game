"""Rundensteuerung: Spielerwechsel, Würfe, Kategoriewahl, Spielende."""
from __future__ import annotations

from typing import List

from .category import ScoreCategory
from .dice import Dice, DiceCup, ROLLS_PER_TURN
from .player import Player


class Game:
    """Steuert eine Partie mit mehreren Spielern und einem gemeinsamen DiceCup."""

    def __init__(self, player_names: List[str], categories: List[ScoreCategory]) -> None:
        self._categories = categories
        self._players: List[Player] = [Player(name, categories) for name in player_names]
        self._current_player_index = 0
        self._dice_cup = DiceCup()

    def current_player(self) -> Player:
        return self._players[self._current_player_index]

    def dice(self) -> List[Dice]:
        return self._dice_cup.dice

    def roll_dice(self) -> None:
        if self._dice_cup.rolls_left == ROLLS_PER_TURN:
            self._dice_cup.roll_all()
        else:
            self._dice_cup.roll_unheld()

    def choose_category(self, category: ScoreCategory) -> None:
        score = category.calculate_score(self._dice_cup.values())
        self.current_player().score_card.set_score(category, score)
        self.next_turn()

    def next_turn(self) -> None:
        self._dice_cup.reset()
        self._current_player_index = (self._current_player_index + 1) % len(self._players)

    def is_over(self) -> bool:
        return all(
            player.score_card.is_filled(category)
            for player in self._players
            for category in self._categories
        )

    def winner(self) -> Player:
        return max(self._players, key=lambda player: player.score_card.total_score())

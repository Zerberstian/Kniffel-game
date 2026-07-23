"""Bindeglied zwischen Game (Spiellogik) und App (GUI) - einzige Klasse, die beide Seiten kennt."""
from __future__ import annotations

from typing import Any

from ..game.category import ScoreCategory
from ..game.dice import ROLLS_PER_TURN
from ..game.game import Game


class GameConnector:
    """Leitet Nutzeraktionen der GUI an Game weiter und aktualisiert danach die View."""

    def __init__(self, game: Game, view: Any) -> None:
        self._game = game
        self._view = view

    def on_roll(self) -> None:
        if self._game.rolls_left() <= 0:
            return
        self._game.roll_dice()
        self.refresh_view()

    def on_hold_toggle(self, dice_id: int) -> None:
        if self._game.rolls_left() == ROLLS_PER_TURN:
            return
        die = next(d for d in self._game.dice() if d.dice_id == dice_id)
        if die.held:
            if die.locked:
                return
            die.release()
        else:
            die.hold()
        self.refresh_view()

    def on_category_chosen(self, category: ScoreCategory) -> None:
        if self._game.current_player().score_card.is_filled(category):
            return
        score = category.calculate_score(self._game.dice_values())
        if score == 0 and not self._view.confirm_zero_score(category.name):
            return
        self._game.choose_category(category)
        self.refresh_view()

    def refresh_view(self) -> None:
        rolls_left = self._game.rolls_left()
        has_rolled = rolls_left < ROLLS_PER_TURN
        dice_values = self._game.dice_values() if has_rolled else None
        self._view.dice_view.render(self._game.dice(), has_rolled=has_rolled)
        self._view.scorecard_view.render(self._game.current_player().score_card, dice_values)
        self._view.set_rolls_remaining(rolls_left)
        self._view.set_active_player_color(self._game.current_player_index)
        self._view.set_turn_status(self._game.current_player().name, rolls_left)
        if self._game.is_over():
            winner = self._game.winner()
            self._view.show_winner(winner.name, winner.score_card.total_score())

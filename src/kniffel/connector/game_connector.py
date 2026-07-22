"""Bindeglied zwischen Game (Spiellogik) und App (GUI) - einzige Klasse, die beide Seiten kennt."""
from __future__ import annotations

from typing import Any

from ..game.category import ScoreCategory
from ..game.game import Game


class GameConnector:
    """Leitet Nutzeraktionen der GUI an Game weiter und aktualisiert danach die View."""

    def __init__(self, game: Game, view: Any) -> None:
        self._game = game
        self._view = view

    def on_roll(self) -> None:
        self._game.roll_dice()
        self.refresh_view()

    def on_hold_toggle(self, dice_id: int) -> None:
        die = next(d for d in self._game.dice() if d.dice_id == dice_id)
        die.release() if die.held else die.hold()
        self.refresh_view()

    def on_category_chosen(self, category: ScoreCategory) -> None:
        self._game.choose_category(category)
        self.refresh_view()

    def refresh_view(self) -> None:
        self._view.dice_view.render(self._game.dice())
        self._view.scorecard_view.render(self._game.current_player().score_card)
        if self._game.is_over():
            winner = self._game.winner()
            self._view.show_winner(winner.name, winner.score_card.total_score())

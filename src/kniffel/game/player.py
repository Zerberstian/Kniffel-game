"""Spieler: Name und eigene Punktekarte."""
from __future__ import annotations

from typing import List

from .category import ScoreCategory
from .score_card import ScoreCard


class Player:
    """Ein Spieler mit Name und einer eigenen ScoreCard."""

    def __init__(self, name: str, categories: List[ScoreCategory]) -> None:
        self._name = name
        self._score_card = ScoreCard(categories)

    @property
    def name(self) -> str:
        return self._name

    @property
    def score_card(self) -> ScoreCard:
        return self._score_card

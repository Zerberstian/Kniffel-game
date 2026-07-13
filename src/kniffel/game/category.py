"""Bewertungskategorien für Kniffel: eine Klasse je Kategorie, Polymorphie über calculate_score()."""
from __future__ import annotations

from abc import ABC, abstractmethod
from collections import Counter
from typing import List

FULL_HOUSE_SCORE = 25
SMALL_STRAIGHT_SCORE = 30
LARGE_STRAIGHT_SCORE = 40
KNIFFEL_SCORE = 50

_SMALL_STRAIGHT_SEQUENCES = ({1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6}) 
_LARGE_STRAIGHT_SEQUENCES = ({1, 2, 3, 4, 5}, {2, 3, 4, 5, 6})


class ScoreCategory(ABC):
    """Basisklasse aller Bewertungskategorien."""

    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def calculate_score(self, dice: List[int]) -> int:
        ...


class NumberCategory(ScoreCategory):
    """Deckt Einer bis Sechser über einen Parameter ab statt über 6 Klassen."""

    def __init__(self, name: str, target: int) -> None:
        super().__init__(name)
        self._target = target

    def calculate_score(self, dice: List[int]) -> int:
        return dice.count(self._target) * self._target


class ThreeOfAKind(ScoreCategory):
    def calculate_score(self, dice: List[int]) -> int:
        if max(Counter(dice).values()) >= 3:
            return sum(dice)
        return 0


class FourOfAKind(ScoreCategory):
    def calculate_score(self, dice: List[int]) -> int:
        if max(Counter(dice).values()) >= 4:
            return sum(dice)
        return 0


class FullHouse(ScoreCategory):
    def calculate_score(self, dice: List[int]) -> int:
        if sorted(Counter(dice).values()) == [2, 3]:
            return FULL_HOUSE_SCORE
        return 0


class SmallStraight(ScoreCategory):
    def calculate_score(self, dice: List[int]) -> int:
        values = set(dice)
        if any(sequence <= values for sequence in _SMALL_STRAIGHT_SEQUENCES):
            return SMALL_STRAIGHT_SCORE
        return 0


class LargeStraight(ScoreCategory):
    def calculate_score(self, dice: List[int]) -> int:
        if set(dice) in _LARGE_STRAIGHT_SEQUENCES:
            return LARGE_STRAIGHT_SCORE
        return 0


class Kniffel(ScoreCategory):
    def calculate_score(self, dice: List[int]) -> int:
        if len(set(dice)) == 1:
            return KNIFFEL_SCORE
        return 0


class Chance(ScoreCategory):
    def calculate_score(self, dice: List[int]) -> int:
        return sum(dice)

"""Punktekarte eines Spielers: Kategorie-Einträge, Bonusregel, Gesamtsumme."""
from __future__ import annotations

from typing import Dict, List, Optional

from .category import NumberCategory, ScoreCategory

UPPER_SECTION_BONUS_THRESHOLD = 63
UPPER_SECTION_BONUS = 35


class ScoreCard:
    """Hält je Kategorie höchstens einen eingetragenen Wert (None = noch offen)."""

    def __init__(self, categories: List[ScoreCategory]) -> None:
        self._entries: Dict[ScoreCategory, Optional[int]] = {category: None for category in categories}

    def set_score(self, category: ScoreCategory, value: int) -> None:
        if category not in self._entries:
            raise KeyError(f"Unbekannte Kategorie: {category.name}")
        if self.is_filled(category):
            raise ValueError(f"{category.name} ist bereits eingetragen")
        self._entries[category] = value

    def is_filled(self, category: ScoreCategory) -> bool:
        return self._entries.get(category) is not None

    def score(self, category: ScoreCategory) -> Optional[int]:
        return self._entries.get(category)

    def upper_section_bonus(self) -> int:
        upper_sum = sum(
            value
            for category, value in self._entries.items()
            if value is not None and isinstance(category, NumberCategory)
        )
        return UPPER_SECTION_BONUS if upper_sum >= UPPER_SECTION_BONUS_THRESHOLD else 0

    def total_score(self) -> int:
        entered = sum(value for value in self._entries.values() if value is not None)
        return entered + self.upper_section_bonus()

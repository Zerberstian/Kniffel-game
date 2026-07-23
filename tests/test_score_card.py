import logging
import unittest

from _support import configure_logging
from kniffel.game.category import Chance, NumberCategory
from kniffel.game.score_card import ScoreCard

logger = logging.getLogger(__name__)


def setUpModule() -> None:
    configure_logging()


class ScoreCardTest(unittest.TestCase):
    def setUp(self) -> None:
        self.einer = NumberCategory("Einer", 1)
        self.sechser = NumberCategory("Sechser", 6)
        self.chance = Chance("Chance")
        self.card = ScoreCard([self.einer, self.sechser, self.chance])

    def test_new_entries_are_unfilled(self) -> None:
        self.assertFalse(self.card.is_filled(self.einer))

    def test_set_score_marks_filled(self) -> None:
        self.card.set_score(self.sechser, 24)
        logger.info("Sechser eingetragen: 24 -> gefüllt=%s", self.card.is_filled(self.sechser))
        self.assertTrue(self.card.is_filled(self.sechser))

    def test_set_score_twice_raises(self) -> None:
        self.card.set_score(self.einer, 3)
        with self.assertRaises(ValueError):
            self.card.set_score(self.einer, 2)

    def test_set_score_unknown_category_raises(self) -> None:
        outsider = Chance("Fremd")
        with self.assertRaises(KeyError):
            self.card.set_score(outsider, 10)

    def test_total_score_sums_only_filled_entries(self) -> None:
        self.card.set_score(self.einer, 3)
        self.card.set_score(self.chance, 20)
        logger.info("Gesamt ohne Sechser -> %d", self.card.total_score())
        self.assertEqual(self.card.total_score(), 23)


class UpperSectionBonusTest(unittest.TestCase):
    def test_bonus_awarded_at_threshold(self) -> None:
        einer = NumberCategory("Einer", 1)
        sechser = NumberCategory("Sechser", 6)
        card = ScoreCard([einer, sechser])
        card.set_score(einer, 25)
        card.set_score(sechser, 38)
        logger.info(
            "Obere Summe=63 -> Bonus=%d, Gesamt=%d",
            card.upper_section_bonus(), card.total_score(),
        )
        self.assertEqual(card.upper_section_bonus(), 35)
        self.assertEqual(card.total_score(), 98)

    def test_no_bonus_below_threshold(self) -> None:
        einer = NumberCategory("Einer", 1)
        sechser = NumberCategory("Sechser", 6)
        card = ScoreCard([einer, sechser])
        card.set_score(einer, 25)
        card.set_score(sechser, 37)
        self.assertEqual(card.upper_section_bonus(), 0)

    def test_lower_section_does_not_count_toward_bonus(self) -> None:
        einer = NumberCategory("Einer", 1)
        chance = Chance("Chance")
        card = ScoreCard([einer, chance])
        card.set_score(einer, 10)
        card.set_score(chance, 100)
        logger.info("Chance zählt nicht zur oberen Sektion -> Bonus=%d", card.upper_section_bonus())
        self.assertEqual(card.upper_section_bonus(), 0)


class ExtraKniffelBonusTest(unittest.TestCase):
    def test_no_bonus_without_extra_kniffel(self) -> None:
        card = ScoreCard([Chance("Chance")])
        self.assertEqual(card.lower_section_bonus(), 0)

    def test_each_extra_kniffel_adds_fifty(self) -> None:
        card = ScoreCard([Chance("Chance")])
        card.add_extra_kniffel_bonus()
        card.add_extra_kniffel_bonus()
        logger.info("Zwei Zusatz-Kniffel -> Bonus Unten=%d", card.lower_section_bonus())
        self.assertEqual(card.lower_section_bonus(), 100)

    def test_total_score_includes_lower_section_bonus(self) -> None:
        chance = Chance("Chance")
        card = ScoreCard([chance])
        card.set_score(chance, 20)
        card.add_extra_kniffel_bonus()
        self.assertEqual(card.total_score(), 70)


if __name__ == "__main__":
    unittest.main(verbosity=2)

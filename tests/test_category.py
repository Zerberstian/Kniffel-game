import logging
import sys
import unittest
from pathlib import Path

_TESTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_TESTS_DIR.parent / "src"))
sys.path.insert(0, str(_TESTS_DIR))

from _support import configure_logging
from kniffel.game.category import (
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

logger = logging.getLogger(__name__)


def setUpModule() -> None:
    configure_logging()


class NumberCategoryTest(unittest.TestCase):
    def test_counts_only_target(self) -> None:
        score = NumberCategory("Sechser", 6).calculate_score([6, 6, 3, 1, 6])
        logger.info("Sechser auf [6,6,3,1,6] -> %d", score)
        self.assertEqual(score, 18)

    def test_zero_without_match(self) -> None:
        self.assertEqual(NumberCategory("Sechser", 6).calculate_score([1, 2, 3, 4, 5]), 0)


class OfAKindTest(unittest.TestCase):
    def test_three_sums_all_dice(self) -> None:
        score = ThreeOfAKind("Dreierpasch").calculate_score([3, 3, 3, 2, 1])
        logger.info("Dreierpasch auf [3,3,3,2,1] -> %d", score)
        self.assertEqual(score, 12)

    def test_three_zero_without_triple(self) -> None:
        self.assertEqual(ThreeOfAKind("Dreierpasch").calculate_score([1, 2, 3, 4, 5]), 0)

    def test_four_sums_all_dice(self) -> None:
        score = FourOfAKind("Viererpasch").calculate_score([4, 4, 4, 4, 2])
        logger.info("Viererpasch auf [4,4,4,4,2] -> %d", score)
        self.assertEqual(score, 18)

    def test_four_zero_without_quad(self) -> None:
        self.assertEqual(FourOfAKind("Viererpasch").calculate_score([1, 1, 1, 2, 2]), 0)


class FullHouseTest(unittest.TestCase):
    def test_pair_and_triple_scores_fixed(self) -> None:
        score = FullHouse("Full House").calculate_score([2, 2, 3, 3, 3])
        logger.info("Full House auf [2,2,3,3,3] -> %d", score)
        self.assertEqual(score, 25)

    def test_five_of_a_kind_is_not_full_house(self) -> None:
        self.assertEqual(FullHouse("Full House").calculate_score([4, 4, 4, 4, 4]), 0)


class StraightTest(unittest.TestCase):
    def test_small_ignores_extra_duplicate(self) -> None:
        score = SmallStraight("Kleine Straße").calculate_score([2, 3, 4, 5, 5])
        logger.info("Kleine Straße auf [2,3,4,5,5] -> %d", score)
        self.assertEqual(score, 30)

    def test_small_zero_on_gap(self) -> None:
        self.assertEqual(SmallStraight("Kleine Straße").calculate_score([1, 1, 2, 3, 5]), 0)

    def test_large_exact_sequence(self) -> None:
        score = LargeStraight("Große Straße").calculate_score([2, 3, 4, 5, 6])
        logger.info("Große Straße auf [2,3,4,5,6] -> %d", score)
        self.assertEqual(score, 40)

    def test_large_zero_with_duplicate(self) -> None:
        self.assertEqual(LargeStraight("Große Straße").calculate_score([1, 2, 3, 4, 4]), 0)


class KniffelAndChanceTest(unittest.TestCase):
    def test_kniffel_all_equal(self) -> None:
        score = Kniffel("Kniffel").calculate_score([5, 5, 5, 5, 5])
        logger.info("Kniffel auf [5,5,5,5,5] -> %d", score)
        self.assertEqual(score, 50)

    def test_kniffel_zero_without_five_equal(self) -> None:
        self.assertEqual(Kniffel("Kniffel").calculate_score([5, 5, 5, 5, 4]), 0)

    def test_chance_sums_everything(self) -> None:
        score = Chance("Chance").calculate_score([1, 2, 3, 4, 5])
        logger.info("Chance auf [1,2,3,4,5] -> %d", score)
        self.assertEqual(score, 15)


class PolymorphismTest(unittest.TestCase):
    def test_uniform_call_across_subclasses(self) -> None:
        categories: list[ScoreCategory] = [
            NumberCategory("Sechser", 6),
            ThreeOfAKind("Dreierpasch"),
            Chance("Chance"),
        ]
        dice = [6, 6, 6, 2, 1]
        scores = [category.calculate_score(dice) for category in categories]
        logger.info("gleicher Aufruf calculate_score() über 3 Unterklassen -> %s", scores)
        self.assertEqual(scores, [18, 21, 21])

    def test_abstract_class_cannot_be_instantiated(self) -> None:
        with self.assertRaises(TypeError):
            ScoreCategory("Basis")  # type: ignore[abstract]


if __name__ == "__main__":
    unittest.main(verbosity=2)

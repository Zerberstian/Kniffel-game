import logging
import unittest

from _support import configure_logging
from kniffel.game.category import Chance, Kniffel, NumberCategory
from kniffel.game.dice import ROLLS_PER_TURN
from kniffel.game.game import Game

logger = logging.getLogger(__name__)


def setUpModule() -> None:
    configure_logging()


class GameTest(unittest.TestCase):
    def setUp(self) -> None:
        self.categories = [NumberCategory("Sechser", 6), Chance("Chance")]
        self.game = Game(["Alice", "Bob"], self.categories)

    def test_current_player_starts_with_first(self) -> None:
        self.assertEqual(self.game.current_player().name, "Alice")

    def test_roll_dice_consumes_a_roll(self) -> None:
        self.game.roll_dice()
        self.assertEqual(self.game._dice_cup.rolls_left, ROLLS_PER_TURN - 1)

    def test_choose_category_scores_and_advances_turn(self) -> None:
        self.game.roll_dice()
        chance = self.categories[1]
        self.game.choose_category(chance)
        logger.info("Alice Gesamt=%d, jetzt am Zug: %s", self.game._players[0].score_card.total_score(), self.game.current_player().name)
        self.assertTrue(self.game._players[0].score_card.is_filled(chance))
        self.assertEqual(self.game.current_player().name, "Bob")

    def test_extra_kniffel_after_first_grants_lower_section_bonus(self) -> None:
        categories = [Kniffel("Kniffel"), Chance("Chance")]
        game = Game(["Alice"], categories)
        score_card = game.current_player().score_card

        for die in game.dice():
            die._value = 6
        game.choose_category(categories[0])
        self.assertEqual(score_card.score(categories[0]), 50)
        self.assertEqual(score_card.lower_section_bonus(), 0)

        for die in game.dice():
            die._value = 3
        game.choose_category(categories[1])
        self.assertEqual(score_card.lower_section_bonus(), 50)

    def test_is_over_and_winner(self) -> None:
        for category in self.categories:
            for _ in range(2):  # einmal pro Spieler
                self.game.roll_dice()
                self.game.choose_category(category)
        self.assertTrue(self.game.is_over())
        self.assertIn(self.game.winner().name, ("Alice", "Bob"))


if __name__ == "__main__":
    unittest.main(verbosity=2)

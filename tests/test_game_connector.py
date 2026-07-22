import logging
import unittest

from _support import configure_logging
from kniffel.connector.game_connector import GameConnector
from kniffel.game.category import Chance, NumberCategory
from kniffel.game.game import Game

logger = logging.getLogger(__name__)


def setUpModule() -> None:
    configure_logging()


class FakeSubView:
    def __init__(self) -> None:
        self.rendered = None

    def render(self, data) -> None:
        self.rendered = data


class FakeView:
    def __init__(self) -> None:
        self.dice_view = FakeSubView()
        self.scorecard_view = FakeSubView()
        self.winner = None

    def show_winner(self, name, score) -> None:
        self.winner = (name, score)


class GameConnectorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.categories = [NumberCategory("Sechser", 6), Chance("Chance")]
        self.game = Game(["Alice", "Bob"], self.categories)
        self.view = FakeView()
        self.connector = GameConnector(self.game, self.view)

    def test_on_roll_rolls_dice_and_refreshes_view(self) -> None:
        self.connector.on_roll()
        logger.info("Würfelwerte nach on_roll: %s", [die.value for die in self.view.dice_view.rendered])
        self.assertEqual(len(self.view.dice_view.rendered), 5)
        self.assertIsNotNone(self.view.scorecard_view.rendered)

    def test_on_hold_toggle_toggles_the_given_die(self) -> None:
        self.connector.on_roll()
        die = self.game.dice()[0]
        self.assertFalse(die.held)
        self.connector.on_hold_toggle(0)
        self.assertTrue(die.held)
        self.connector.on_hold_toggle(0)
        self.assertFalse(die.held)

    def test_on_category_chosen_scores_and_advances_turn(self) -> None:
        self.connector.on_roll()
        self.connector.on_category_chosen(self.categories[1])
        self.assertEqual(self.game.current_player().name, "Bob")
        self.assertIsNone(self.view.winner)

    def test_game_over_reports_winner_to_view(self) -> None:
        """Die Züge wechseln pro Spieler, daher wird category[t // num_players] mit jedem Zug gekoppelt,
        um jede Kategorie für jeden Spieler genau einmal in allen Zügen auszufüllen."""
        num_players = len(self.game._players)
        for turn in range(num_players * len(self.categories)):
            self.connector.on_roll()
            self.connector.on_category_chosen(self.categories[turn // num_players])
        self.assertIsNotNone(self.view.winner)
        name, score = self.view.winner
        self.assertEqual(self.game.winner().name, name)
        self.assertEqual(self.game.winner().score_card.total_score(), score)


if __name__ == "__main__":
    unittest.main(verbosity=2)

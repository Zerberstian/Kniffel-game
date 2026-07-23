import logging
import unittest

from _support import configure_logging
from kniffel.connector.game_connector import GameConnector
from kniffel.game.category import Chance, NumberCategory
from kniffel.game.dice import ROLLS_PER_TURN
from kniffel.game.game import Game

logger = logging.getLogger(__name__)


def setUpModule() -> None:
    configure_logging()


class FakeSubView:
    def __init__(self) -> None:
        self.rendered = None
        self.has_rolled = None

    def render(self, data, has_rolled: bool = True) -> None:
        self.rendered = data
        self.has_rolled = has_rolled


class FakeView:
    def __init__(self) -> None:
        self.dice_view = FakeSubView()
        self.scorecard_view = FakeSubView()
        self.winner = None
        self.rolls_remaining = None
        self.turn_status = None
        self.active_player_color = None
        self.confirm_zero_score_calls = []
        self.confirm_zero_score_return = True

    def show_winner(self, name, score) -> None:
        self.winner = (name, score)

    def set_rolls_remaining(self, rolls_left) -> None:
        self.rolls_remaining = rolls_left

    def set_turn_status(self, player_name, rolls_left) -> None:
        self.turn_status = (player_name, rolls_left)

    def set_active_player_color(self, index) -> None:
        self.active_player_color = index

    def confirm_zero_score(self, category_name) -> bool:
        self.confirm_zero_score_calls.append(category_name)
        return self.confirm_zero_score_return


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

    def test_on_hold_toggle_cannot_release_a_locked_die(self) -> None:
        self.connector.on_roll()
        self.connector.on_hold_toggle(0)
        self.connector.on_roll()  # zweiter Wurf sperrt den gehaltenen Würfel
        die = self.game.dice()[0]
        self.assertTrue(die.locked)
        self.connector.on_hold_toggle(0)
        self.assertTrue(die.held)  # darf nicht wieder freigegeben werden

    def test_on_hold_toggle_before_first_roll_is_ignored(self) -> None:
        die = self.game.dice()[0]
        self.connector.on_hold_toggle(0)
        self.assertFalse(die.held)

    def test_refresh_view_sets_turn_status(self) -> None:
        self.connector.on_roll()
        self.assertEqual(self.view.turn_status, ("Alice", self.game.rolls_left()))

    def test_refresh_view_sets_active_player_color(self) -> None:
        self.connector.on_roll()
        self.assertEqual(self.view.active_player_color, 0)
        self.connector.on_category_chosen(self.categories[1])  # Chance kann nie 0 ergeben
        self.assertEqual(self.view.active_player_color, 1)

    def test_on_category_chosen_with_zero_score_asks_for_confirmation(self) -> None:
        self.connector.on_roll()
        for die in self.game.dice():
            die._value = 1
        self.connector.on_category_chosen(self.categories[0])  # Sechser, keine 6 gewürfelt -> 0
        self.assertEqual(self.view.confirm_zero_score_calls, ["Sechser"])
        self.assertTrue(self.game._players[0].score_card.is_filled(self.categories[0]))

    def test_on_category_chosen_with_zero_score_declined_does_not_score(self) -> None:
        self.connector.on_roll()
        for die in self.game.dice():
            die._value = 1
        self.view.confirm_zero_score_return = False
        self.connector.on_category_chosen(self.categories[0])
        self.assertFalse(self.game._players[0].score_card.is_filled(self.categories[0]))
        self.assertEqual(self.game.current_player().name, "Alice")

    def test_on_category_chosen_scores_and_advances_turn(self) -> None:
        self.connector.on_roll()
        self.connector.on_category_chosen(self.categories[1])
        self.assertEqual(self.game.current_player().name, "Bob")
        self.assertIsNone(self.view.winner)

    def test_on_roll_beyond_rolls_left_is_ignored(self) -> None:
        for _ in range(ROLLS_PER_TURN):
            self.connector.on_roll()
        self.assertEqual(self.game.rolls_left(), 0)
        self.connector.on_roll()  # 4. Wurf darf nicht crashen und nichts verändern
        self.assertEqual(self.game.rolls_left(), 0)
        self.assertEqual(self.view.rolls_remaining, 0)

    def test_on_category_chosen_for_filled_category_is_ignored(self) -> None:
        category = self.categories[0]
        self.connector.on_roll()
        self.connector.on_category_chosen(category)  # Alice füllt category
        self.connector.on_roll()
        self.connector.on_category_chosen(category)  # Bob füllt category, zurück zu Alice
        alice_score = self.game._players[0].score_card.score(category)

        self.connector.on_roll()
        self.connector.on_category_chosen(category)  # Alice bereits belegt, darf nicht crashen/wechseln

        self.assertEqual(self.game.current_player().name, "Alice")
        self.assertEqual(self.game._players[0].score_card.score(category), alice_score)

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

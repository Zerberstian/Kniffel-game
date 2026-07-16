import logging
import unittest

from _support import configure_logging
from kniffel.game.category import Chance, NumberCategory
from kniffel.game.player import Player

logger = logging.getLogger(__name__)


def setUpModule() -> None:
    configure_logging()


class PlayerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.categories = [NumberCategory("Sechser", 6), Chance("Chance")]

    def test_player_has_name(self) -> None:
        player = Player("Alice", self.categories)
        self.assertEqual(player.name, "Alice")

    def test_player_has_own_score_card(self) -> None:
        player = Player("Alice", self.categories)
        logger.info("neuer Spieler '%s', Gesamt=%d", player.name, player.score_card.total_score())
        self.assertEqual(player.score_card.total_score(), 0)

    def test_players_have_independent_score_cards(self) -> None:
        alice = Player("Alice", self.categories)
        bob = Player("Bob", self.categories)
        alice.score_card.set_score(self.categories[1], 20)
        logger.info(
            "Alice Gesamt=%d, Bob Gesamt=%d (gleiche Kategorien, unabhängige Karten)",
            alice.score_card.total_score(), bob.score_card.total_score(),
        )
        self.assertEqual(alice.score_card.total_score(), 20)
        self.assertEqual(bob.score_card.total_score(), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)

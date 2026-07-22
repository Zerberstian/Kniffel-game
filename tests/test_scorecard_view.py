import tkinter as tk
import unittest

from _support import configure_logging
from kniffel.game.category import (
    Chance,
    FourOfAKind,
    FullHouse,
    Kniffel,
    LargeStraight,
    NumberCategory,
    SmallStraight,
    ThreeOfAKind,
)
from kniffel.game.score_card import ScoreCard
from kniffel.gui.Scorecard_view import NUMBER_OF_CATEGORIES, ScoreFrame, ScorecardView


def setUpModule() -> None:
    configure_logging()


class ScorecardViewTest(unittest.TestCase):
    def setUp(self) -> None:
        self.root = tk.Tk()
        self.root.withdraw()
        self.frames = [ScoreFrame(self.root, i) for i in range(NUMBER_OF_CATEGORIES)]

        self.einer = NumberCategory("Einer", 1)
        self.dreierpasch = ThreeOfAKind("Dreierpasch")
        self.categories = [
            self.einer,
            NumberCategory("Zweier", 2),
            NumberCategory("Dreier", 3),
            NumberCategory("Vierer", 4),
            NumberCategory("Fünfer", 5),
            NumberCategory("Sechser", 6),
            self.dreierpasch,
            FourOfAKind("Viererpasch"),
            FullHouse("Full House"),
            SmallStraight("Kleine Straße"),
            LargeStraight("Große Straße"),
            Kniffel("Kniffel"),
            Chance("Chance"),
        ]
        self.score_card = ScoreCard(self.categories)

        self.chosen = []
        self.view = ScorecardView(self.frames, self.categories, on_category_chosen=self.chosen.append)

    def tearDown(self) -> None:
        self.root.destroy()

    def test_render_shows_filled_scores_and_blanks_open_ones(self) -> None:
        self.score_card.set_score(self.einer, 3)
        self.view.render(self.score_card)
        self.assertEqual(self.frames[0].CategoryButton["text"], "3")
        self.assertEqual(self.frames[1].CategoryButton["text"], "")

    def test_render_shows_upper_bonus_and_total(self) -> None:
        self.score_card.set_score(self.einer, 3)
        self.view.render(self.score_card)
        self.assertEqual(self.frames[6].CategoryButton["text"], "0")
        self.assertEqual(self.frames[15].CategoryButton["text"], "3")

    def test_button_click_reports_matching_category(self) -> None:
        self.frames[7].CategoryButton.invoke()
        self.assertEqual(self.chosen, [self.dreierpasch])


if __name__ == "__main__":
    unittest.main(verbosity=2)

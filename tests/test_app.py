import unittest
from unittest.mock import patch

from _support import configure_logging, get_shared_tk_root
from kniffel.gui.app import App


def setUpModule() -> None:
    configure_logging()


class AppTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = get_shared_tk_root()

    def setUp(self) -> None:
        self.app = App(["Anna", "Ben"], master=self.root)

    def tearDown(self) -> None:
        for child in self.root.winfo_children():
            child.destroy()

    def test_initial_dice_show_placeholder_before_first_roll(self) -> None:
        self.app.root.update()
        texts = [label["text"] for label in self.app.dice_view._active_labels]
        self.assertEqual(texts, ["-", "-", "-", "-", "-"])

    def test_reroll_button_rolls_dice_and_refreshes_view(self) -> None:
        self.app.reroll_button.invoke()
        self.app.root.update()
        texts = [label["text"] for label in self.app.dice_view._active_labels]
        self.assertTrue(all(1 <= int(text) <= 6 for text in texts))

    def test_scorecard_button_click_scores_and_advances_turn(self) -> None:
        self.app.scorecard_view._category_frames[0].CategoryButton.invoke()
        self.app.root.update()
        self.assertEqual(self.app.scorecard_view._category_frames[0].CategoryButton["text"], "")

    def test_rules_text_is_read_only(self) -> None:
        self.assertEqual(str(self.app.rule_text_widget["state"]), "disabled")

    def test_zero_score_choice_asks_for_confirmation(self) -> None:
        self.app.reroll_button.invoke()
        self.app.root.update()
        for die in self.app._game.dice():
            die._value = 2  # Einer-Kategorie: keine Eins gewürfelt -> Score 0

        with patch("kniffel.gui.app.messagebox.askyesno", return_value=True) as mock_confirm:
            self.app.scorecard_view._category_frames[0].CategoryButton.invoke()
            self.app.root.update()

        mock_confirm.assert_called_once()
        einer = self.app.scorecard_view._categories[0]
        self.assertTrue(self.app._game._players[0].score_card.is_filled(einer))


if __name__ == "__main__":
    unittest.main(verbosity=2)

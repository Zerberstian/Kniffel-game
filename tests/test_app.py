import unittest

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

    def test_initial_dice_are_shown_unrolled(self) -> None:
        self.app.root.update()
        texts = [label["text"] for label in self.app.dice_view._labels]
        self.assertEqual(texts, ["1", "1", "1", "1", "1"])

    def test_reroll_button_rolls_dice_and_refreshes_view(self) -> None:
        self.app.reroll_button.invoke()
        self.app.root.update()
        texts = [label["text"].rstrip(" *") for label in self.app.dice_view._labels]
        self.assertTrue(all(1 <= int(text) <= 6 for text in texts))

    def test_scorecard_button_click_scores_and_advances_turn(self) -> None:
        self.app.scorecard_view._category_frames[0].CategoryButton.invoke()
        self.app.root.update()
        self.assertEqual(self.app.scorecard_view._category_frames[0].CategoryButton["text"], "")


if __name__ == "__main__":
    unittest.main(verbosity=2)

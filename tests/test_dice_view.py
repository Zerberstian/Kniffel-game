import unittest

from _support import configure_logging, get_shared_tk_root
from kniffel.game.dice import Dice
from kniffel.gui.dice_view import PLACEHOLDER_TEXT, DiceView


def setUpModule() -> None:
    configure_logging()


class DiceViewTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = get_shared_tk_root()

    def setUp(self) -> None:
        self.clicked = []
        self.view = DiceView(self.root, on_dice_clicked=self.clicked.append)

    def test_render_shows_dice_sorted_by_value(self) -> None:
        low, high = Dice(0), Dice(1)
        low._value, high._value = 2, 5
        self.view.render([high, low])
        texts = [label["text"] for label in self.view._active_labels]
        self.assertEqual(texts, ["2", "5"])

    def test_render_marks_held_dice(self) -> None:
        die = Dice(0)
        die.hold()
        self.view.render([die])
        self.assertEqual(self.view._held_labels[0]["text"], "1")
        self.assertEqual(self.view._active_labels, [])

    def test_clicking_a_die_reports_its_dice_id(self) -> None:
        first, second = Dice(3), Dice(7)
        first._value = second._value = 4
        self.view.render([first, second])
        self.root.update()
        self.view._active_labels[0].event_generate("<Button-1>")
        self.root.update()
        self.assertEqual(self.clicked, [3])

    def test_clicking_a_held_die_reports_its_dice_id(self) -> None:
        die = Dice(5)
        die.hold()
        self.view.render([die])
        self.root.update()
        self.view._held_labels[0].event_generate("<Button-1>")
        self.root.update()
        self.assertEqual(self.clicked, [5])

    def test_disabled_view_ignores_clicks(self) -> None:
        die = Dice(3)
        self.view.render([die])
        self.view.set_enabled(False)
        self.root.update()
        self.view._active_labels[0].event_generate("<Button-1>")
        self.root.update()
        self.assertEqual(self.clicked, [])

    def test_render_shows_placeholder_before_first_roll(self) -> None:
        self.view.render([Dice(0)], has_rolled=False)
        self.assertEqual(self.view._active_labels[0]["text"], PLACEHOLDER_TEXT)


if __name__ == "__main__":
    unittest.main(verbosity=2)

import logging
import unittest

from _support import configure_logging
from kniffel.game.dice import (
    DICE_PER_CUP,
    MAX_VALUE,
    MIN_VALUE,
    ROLLS_PER_TURN,
    Dice,
    DiceCup,
)

logger = logging.getLogger(__name__)


def setUpModule() -> None:
    configure_logging()


class DiceTest(unittest.TestCase):
    def test_initial_state(self) -> None:
        die = Dice()
        logger.info("neuer Würfel: Wert=%d, gehalten=%s", die.value, die.held)
        self.assertFalse(die.held)
        self.assertTrue(MIN_VALUE <= die.value <= MAX_VALUE)

    def test_roll_range(self) -> None:
        die = Dice()
        seen_min, seen_max = MAX_VALUE, MIN_VALUE
        for _ in range(50):
            die.roll()
            seen_min = min(seen_min, die.value)
            seen_max = max(seen_max, die.value)
            self.assertTrue(MIN_VALUE <= die.value <= MAX_VALUE)
        logger.info("50 Würfe: Bereich %d–%d (erlaubt %d–%d)", seen_min, seen_max, MIN_VALUE, MAX_VALUE)

    def test_hold_release(self) -> None:
        die = Dice()
        die.hold()
        held_after_hold = die.held
        die.release()
        logger.info("hold() -> gehalten=%s, release() -> gehalten=%s", held_after_hold, die.held)
        self.assertTrue(held_after_hold)
        self.assertFalse(die.held)


class DiceCupTest(unittest.TestCase):
    def test_initial_values(self) -> None:
        cup = DiceCup()
        logger.info("neuer DiceCup: Werte=%s, Würfe übrig=%d", cup.values(), cup.rolls_left)
        self.assertEqual(len(cup.values()), DICE_PER_CUP)
        self.assertEqual(cup.rolls_left, ROLLS_PER_TURN)

    def test_hold_survives_reroll(self) -> None:
        cup = DiceCup()
        cup.roll_all()
        held_die = cup._dice[0]
        held_die.hold()
        held_value = held_die.value
        for _ in range(cup.rolls_left):
            cup.roll_unheld()
        logger.info(
            "Würfel[0] gehalten bei %d, unverändert nach allen Rerolls -> Werte=%s",
            held_value, cup.values(),
        )
        self.assertEqual(held_die.value, held_value)

    def test_roll_limit(self) -> None:
        cup = DiceCup()
        cup.roll_all()
        self.assertEqual(cup.rolls_left, ROLLS_PER_TURN - 1)
        cup.roll_unheld()
        cup.roll_unheld()
        self.assertEqual(cup.rolls_left, 0)
        with self.assertRaises(RuntimeError):
            cup.roll_unheld()
        logger.info("%d Würfe verbraucht, 4. Wurf wirft RuntimeError (erwartet)", ROLLS_PER_TURN)

    def test_reset(self) -> None:
        cup = DiceCup()
        cup.roll_all()
        cup._dice[0].hold()
        before = (cup.rolls_left, cup._dice[0].held)
        cup.reset()
        logger.info(
            "reset(): (Würfe, gehalten) vorher=%s, nachher=(%d, %s)",
            before, cup.rolls_left, cup._dice[0].held,
        )
        self.assertEqual(cup.rolls_left, ROLLS_PER_TURN)
        self.assertFalse(cup._dice[0].held)


if __name__ == "__main__":
    unittest.main(verbosity=2)

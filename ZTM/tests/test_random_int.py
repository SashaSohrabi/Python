import unittest

from random_int import MAX_NUM, MIN_NUM, run_guess


class TestRandomInt(unittest.TestCase):
    def test_wins_when_guess_matches_answer(self) -> None:
        self.assertTrue(run_guess(5, 5))

    def test_does_not_win_when_guess_differs_from_answer(self) -> None:
        self.assertFalse(run_guess(6, 5))

    def test_rejects_guess_above_maximum(self) -> None:
        self.assertFalse(run_guess(MAX_NUM + 1, 5))

    def test_rejects_guess_bellow_minimum(self) -> None:
        self.assertFalse(run_guess(MIN_NUM - 1, 5))

    def test_rejects_string_guess_with_type_error(self) -> None:
        with self.assertRaises(TypeError):
            run_guess("9", 9)  # type: ignore[reportArgumentType]


if __name__ == "__main__":
    unittest.main()

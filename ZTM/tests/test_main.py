import unittest

from main import do_stuff


class TestDoStuff(unittest.TestCase):
    def setUp(self) -> None:
        print("about to test a function")
        return super().setUp()

    def test_default_param(self) -> None:
        self.assertEqual(do_stuff(), 5)

    def test_adds_five_to_integer(self) -> None:
        self.assertEqual(do_stuff(10), 15)

    def test_converts_numeric_string_and_adds_five(self) -> None:
        self.assertEqual(do_stuff("10"), 15)

    def test_returns_value_error_for_non_numeric_string(self) -> None:
        self.assertIsInstance(do_stuff("string_value"), ValueError)

    def test_returns_type_value_for_none_argument(self) -> None:
        self.assertIsInstance(do_stuff(None), TypeError)  # type: ignore

    def tearDown(self) -> None:
        return super().tearDown()


if __name__ == "__main__":
    unittest.main()

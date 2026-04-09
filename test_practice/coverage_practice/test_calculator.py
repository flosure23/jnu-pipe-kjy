import unittest
import calculator


class TestCalculator(unittest.TestCase):
    def test_add(self):
        self.assertEqual(calculator.add(2, 3), 5)

    def test_divide(self):
        self.assertEqual(calculator.divide(10, 2), 5)


if __name__ == "__main__":
    unittest.main()
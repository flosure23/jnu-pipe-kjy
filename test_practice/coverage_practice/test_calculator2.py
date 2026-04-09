import unittest
import calculator


class TestCalculator2(unittest.TestCase):
    def test_subtract(self):
        self.assertEqual(calculator.subtract(5, 2), 3)


if __name__ == "__main__":
    unittest.main()
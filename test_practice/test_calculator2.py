import unittest
from calculator2 import Calculator


class TestCalculator(unittest.TestCase):
    def setUp(self):
        print(">> setUp 실행됨")
        self.calc = Calculator()

    def tearDown(self):
        print("<< tearDown 실행됨")

    def test_add(self):
        self.assertEqual(self.calc.add(2, 3), 5)

    def test_subtract(self):
        self.assertEqual(self.calc.subtract(5, 3), 2)


if __name__ == "__main__":
    unittest.main()
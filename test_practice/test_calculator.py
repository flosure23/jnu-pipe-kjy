import unittest
from calculator import Calculator


class TestCalculator(unittest.TestCase):
    def test_add(self):
        calc = Calculator()
        self.assertEqual(calc.add(2, 3), 5)   # 일부러 틀리게 작성
        self.assertEqual(calc.add(-1, 1), 0)  # 일부러 틀리게 작성
        self.assertEqual(calc.add(0, 0), 0)


if __name__ == "__main__":
    unittest.main()
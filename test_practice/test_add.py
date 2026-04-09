import unittest
from calculator import Calculator


class TestAdd(unittest.TestCase):
    def test_add_positive(self):
        self.assertEqual(Calculator().add(2, 3), 5)

    def test_add_zero(self):
        self.assertEqual(Calculator().add(0, 0), 0)


if __name__ == "__main__":
    unittest.main()
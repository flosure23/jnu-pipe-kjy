import unittest


class MyTest(unittest.TestCase):
    def test_add(self):
        self.assertEqual(1 + 1, 2)

    def test_add2(self):
        self.assertEqual(1 + 1, 2)

    def calc_add(self):
        self.assertEqual(1 + 1, 2)


if __name__ == "__main__":
    unittest.main()
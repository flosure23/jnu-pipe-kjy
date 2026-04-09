import unittest
from price_service import calculate_price


def stub_get_discount(user_id):
    return 1000


class TestCalculatePriceWithStub(unittest.TestCase):
    def test_discount_applied(self):
        result = calculate_price("user1", 5000, stub_get_discount)
        self.assertEqual(result, 4000)


if __name__ == "__main__":
    unittest.main()
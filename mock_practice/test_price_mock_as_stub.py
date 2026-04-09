import unittest
from unittest.mock import Mock
from price_service import calculate_price


class TestCalculatePriceWithMock(unittest.TestCase):
    def test_discount_applied_with_mock_as_stub(self):
        mock_func = Mock()
        mock_func.return_value = 2000

        result = calculate_price("user123", 8000, mock_func)

        self.assertEqual(result, 6000)


if __name__ == "__main__":
    unittest.main()
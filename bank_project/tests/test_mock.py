import unittest
from unittest.mock import Mock
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from account import Account, InsufficientFundsError


class TestAccountWithMock(unittest.TestCase):
    def setUp(self):
        self.mock_logger = Mock()
        self.account = Account(self.mock_logger)

    def test_deposit_calls_logger(self):
        new_balance = self.account.deposit(200)

        self.assertEqual(new_balance, 200)
        self.assertEqual(self.account.balance, 200)
        self.mock_logger.log.assert_called_with("Deposited 200")

    def test_withdraw_calls_logger(self):
        self.account.deposit(100)
        new_balance = self.account.withdraw(50)

        self.assertEqual(new_balance, 50)
        self.assertEqual(self.account.balance, 50)
        self.mock_logger.log.assert_any_call("Withdrew 50")

    def test_withdraw_insufficient_funds_logs_and_raises(self):
        with self.assertRaises(InsufficientFundsError):
            self.account.withdraw(30)

        self.mock_logger.log.assert_called_with("Withdrawal failed: insufficient funds")


if __name__ == "__main__":
    unittest.main(verbosity=2)
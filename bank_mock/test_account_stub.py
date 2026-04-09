import unittest
from account import Account, InsufficientFundsError
from logger_stub import StubLogger


class TestAccountWithStub(unittest.TestCase):
    def setUp(self):
        self.logger = StubLogger()
        self.account = Account(self.logger)

    def test_deposit_increases_balance(self):
        self.account.deposit(100)
        self.assertEqual(self.account.balance, 100)

    def test_withdraw_raises_error_on_insufficient_funds(self):
        with self.assertRaises(InsufficientFundsError):
            self.account.withdraw(50)


if __name__ == "__main__":
    unittest.main(verbosity=2)
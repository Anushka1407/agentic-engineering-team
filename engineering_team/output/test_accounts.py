import unittest
from accounts import Account, get_share_price

class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = Account("test_user", 1000.0)

    def test_initial_balance(self):
        self.assertEqual(self.account.balance, 1000.0)

    def test_deposit(self):
        self.account.deposit(500.0)
        self.assertEqual(self.account.balance, 1500.0)

    def test_deposit_negative(self):
        with self.assertRaises(ValueError):
            self.account.deposit(-100.0)

    def test_withdraw(self):
        self.account.withdraw(200.0)
        self.assertEqual(self.account.balance, 800.0)

    def test_withdraw_over_balance(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(2000.0)

    def test_buy_shares(self):
        self.account.buy_shares("AAPL", 2)
        self.assertEqual(self.account.portfolio["AAPL"], 2)
        self.assertEqual(self.account.balance, 700.0)

    def test_buy_shares_not_enough_balance(self):
        with self.assertRaises(ValueError):
            self.account.buy_shares("AAPL", 10)

    def test_sell_shares(self):
        self.account.buy_shares("AAPL", 2)
        self.account.sell_shares("AAPL", 1)
        self.assertEqual(self.account.portfolio["AAPL"], 1)
        self.assertEqual(self.account.balance, 850.0)

    def test_sell_shares_not_enough(self):
        with self.assertRaises(ValueError):
            self.account.sell_shares("AAPL", 2)

    def test_calculate_portfolio_value(self):
        self.account.buy_shares("AAPL", 2)
        self.account.deposit(500.0)
        self.assertEqual(self.account.calculate_portfolio_value(), 700.0 + (150.0 * 2))

    def test_calculate_profit_loss(self):
        self.account.buy_shares("AAPL", 2)
        self.assertEqual(self.account.calculate_profit_loss(), (150.0 * 2 + 1000.0) - 1000.0)

    def test_get_holdings(self):
        self.assertEqual(self.account.get_holdings(), {})
        self.account.buy_shares("AAPL", 2)
        self.assertEqual(self.account.get_holdings(), {"AAPL": 2})

    def test_get_transactions(self):
        self.account.deposit(500.0)
        self.account.withdraw(200.0)
        self.assertEqual(len(self.account.get_transactions()), 2)

if __name__ == '__main__':
    unittest.main()
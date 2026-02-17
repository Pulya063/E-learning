import unittest

from ab4a25f0ae4b401dafbcd9de25cb5cfc.app import *

class TestBasic(unittest.TestCase):
    def test_deposit_positive(self):
        account = BankAccount()
        account.deposit(100)
        self.assertEqual(account.get_balance(), 100)

    def test_deposit_negative(self):
        account = BankAccount()
        with self.assertRaises(ValueError):
            account.deposit(-50)
        self.assertEqual(account.get_balance(), 0)

    def test_deposit_zero(self):
        account = BankAccount()
        with self.assertRaises(ValueError):
            account.deposit(0)
        self.assertEqual(account.get_balance(), 0)

    def test_withdraw_positive(self):
        account = BankAccount(100)
        account.withdraw(50)
        self.assertEqual(account.get_balance(), 50)

    def test_withdraw_negative(self):
        account = BankAccount(100)
        with self.assertRaises(ValueError):
            account.withdraw(-50)
        self.assertEqual(account.get_balance(), 100)

    def test_withdraw_zero(self):
        account = BankAccount(100)
        with self.assertRaises(ValueError):
            account.withdraw(0)
        self.assertEqual(account.get_balance(), 100)

    def test_withdraw_insufficient_funds(self):
        account = BankAccount(100)
        with self.assertRaises(InsufficientFunds):
            account.withdraw(150)
        self.assertEqual(account.get_balance(), 100)

    def test_transfer_positive(self):
        first_account = BankAccount(100)
        second_account = BankAccount(50)
        first_account.transfer(second_account, 30)
        self.assertEqual(first_account.get_balance(), 70)
        self.assertEqual(second_account.get_balance(), 80)

    def test_transfer_type_error(self):
        first_account = BankAccount(100)
        with self.assertRaises(TypeError):
            first_account.transfer("not an account", 30)
        self.assertEqual(first_account.get_balance(), 100)

    def test_transfer_negative(self):
        first_account = BankAccount(100)
        second_account = BankAccount(50)
        with self.assertRaises(ValueError):
            first_account.transfer(second_account, -30)
        self.assertEqual(first_account.get_balance(), 100)
        self.assertEqual(second_account.get_balance(), 50)

    def test_transfer_zero(self):
        first_account = BankAccount(100)
        second_account = BankAccount(50)
        with self.assertRaises(ValueError):
            first_account.transfer(second_account, 0)
        self.assertEqual(first_account.get_balance(), 100)
        self.assertEqual(second_account.get_balance(), 50)

    def test_transfer_insufficient_funds(self):
        first_account = BankAccount(100)
        second_account = BankAccount(50)
        with self.assertRaises(InsufficientFunds):
            first_account.transfer(second_account, 150)
        self.assertEqual(first_account.get_balance(), 100)
        self.assertEqual(second_account.get_balance(), 50)

    def test_initial_balance(self):
        account = BankAccount(200)
        self.assertEqual(account.get_balance(), 200)

    def test_initial_balance_negative(self):
        account = BankAccount(-100)
        self.assertEqual(account.get_balance(), -100)

    def test_initial_balance_zero(self):
        account = BankAccount(0)
        self.assertEqual(account.get_balance(), 0)

if __name__ == '__main__':
    unittest.main()

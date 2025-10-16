from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", "12345678901")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0.0
        assert account.pesel == "12345678901"
    
    def test_pesel_too_long(self):
        account = Account("Jane", "Doe", "1234567890193245")
        assert account.pesel == 'Invalid'
    
    def test_pesel_too_short(self):
        account = Account("Jane", "Doe", "123")
        assert account.pesel == 'Invalid'

    def test_pesel_none(self):
        account = Account("Jane", "Doe", None)
        assert account.pesel == 'Invalid'

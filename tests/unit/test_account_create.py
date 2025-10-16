from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", "12345678901")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0.0
        assert account.pesel == "12345678901"
    
    def test_pesel_too_long(self):
        account = Account("John", "Doe", "1234567890193245")
        assert account.pesel == 'Invalid'
    
    def test_pesel_too_short(self):
        account = Account("John", "Doe", "123")
        assert account.pesel == 'Invalid'

    def test_pesel_none(self):
        account = Account("John", "Doe", None)
        assert account.pesel == 'Invalid'
    

    def test_correct_promo_code(self):
        account = Account("John", "Doe", "12345678901", promo_code="PROM_123")
        assert account.balance == 50.0

    def test_promo_code_suffix_too_long(self):
        account = Account("John", "Doe", "12345678901", promo_code="PROM_XYZZ")
        assert account.balance == 0.0
    
    def test_promo_code_suffix_too_short(self):
        account = Account("John", "Doe", "12345678901", promo_code="PROM_XY")
        assert account.balance == 0.0

    def test_promo_code_wrong_prefix(self):
        account = Account("John", "Doe", "12345678901", promo_code="PRO_XYZ")
        assert account.balance == 0.0

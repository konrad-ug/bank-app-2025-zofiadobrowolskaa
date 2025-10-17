from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", "12345678901")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0.0           # feature 1
        assert account.pesel == "12345678901"   # feature 2
    
    # feature 3
    def test_pesel_too_long(self):
        account = Account("John", "Doe", "1234567890193245")
        assert account.pesel == 'Invalid'
    
    def test_pesel_too_short(self):
        account = Account("John", "Doe", "123")
        assert account.pesel == 'Invalid'

    def test_pesel_none(self):
        account = Account("John", "Doe", None)
        assert account.pesel == 'Invalid'
    
    # feature 4
    def test_correct_promo_code(self):
        account = Account("John", "Doe", "64051212345", promo_code="PROM_XYZ")
        assert account.balance == 50.0

    def test_promo_code_suffix_too_long(self):
        account = Account("John", "Doe", "64051212345", promo_code="PROM_XYZZ")
        assert account.balance == 0.0

    def test_promo_code_suffix_too_short(self):
        account = Account("John", "Doe", "64051212345", promo_code="PROM_XY")
        assert account.balance == 0.0

    def test_promo_code_wrong_prefix(self):
        account = Account("John", "Doe", "64051212345", promo_code="PRO-XYZ")
        assert account.balance == 0.0

    # feature 5
    def test_birth_year_1800s(self):
        account = Account("John", "Doe", "86910112345")
        assert account.get_birth_year_from_pesel("86910112345") == 1886

    def test_birth_year_1900s(self):
        account = Account("John", "Doe", "64051212345")
        assert account.get_birth_year_from_pesel("64051212345") == 1964

    def test_birth_year_2000s(self):
        account = Account("John", "Doe", "05210112345")
        assert account.get_birth_year_from_pesel("05210112345") == 2005

    def test_invalid_month(self):
        account = Account("John", "Doe", "99130112345")
        assert account.get_birth_year_from_pesel("99130112345") is None

    def test_person_born_after_1960_gets_promo(self):
        account = Account("John", "Doe", "64051212345")
        assert account.can_receive_promo("64051212345") is True

    def test_person_born_before_1960_no_promo(self):
        account = Account("John", "Doe", "59010112345")
        assert account.can_receive_promo("59010112345") is False

    def test_account_with_promo_and_young_age_gets_promo(self):
        account = Account("John", "Doe", "64051212345", promo_code="PROM_XYZ")
        assert account.balance == 50.0

    def test_account_with_promo_and_old_age_gets_no_promo(self):
        account = Account("John", "Doe", "59010112345", promo_code="PROM_XYZ")
        assert account.balance == 0.0
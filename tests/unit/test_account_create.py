from src.company_account import CompanyAccount
from src.personal_account import PersonalAccount
class TestAccount:
    def test_account_creation(self):
        account = PersonalAccount("John", "Doe", "12345678901")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0.0           # feature 1
        assert account.pesel == "12345678901"   # feature 2
    
    # feature 3
    def test_pesel_too_long(self):
        account = PersonalAccount("John", "Doe", "1234567890193245")
        assert account.pesel == 'Invalid'
    
    def test_pesel_too_short(self):
        account = PersonalAccount("John", "Doe", "123")
        assert account.pesel == 'Invalid'

    def test_pesel_none(self):
        account = PersonalAccount("John", "Doe", None)
        assert account.pesel == 'Invalid'
    
    # feature 4
    def test_correct_promo_code(self):
        account = PersonalAccount("John", "Doe", "64051212345", promo_code="PROM_XYZ")
        assert account.balance == 50.0

    def test_promo_code_suffix_too_long(self):
        account = PersonalAccount("John", "Doe", "64051212345", promo_code="PROM_XYZZ")
        assert account.balance == 0.0

    def test_promo_code_suffix_too_short(self):
        account = PersonalAccount("John", "Doe", "64051212345", promo_code="PROM_XY")
        assert account.balance == 0.0

    def test_promo_code_wrong_prefix(self):
        account = PersonalAccount("John", "Doe", "64051212345", promo_code="PROM-XYZ")
        assert account.balance == 0.0

    # feature 5
    def test_birth_year_1800s(self):
        account = PersonalAccount("John", "Doe", "86910112345")
        assert account.get_birth_year_from_pesel("86910112345") == 1886

    def test_birth_year_1900s(self):
        account = PersonalAccount("John", "Doe", "64051212345")
        assert account.get_birth_year_from_pesel("64051212345") == 1964

    def test_birth_year_2000s(self):
        account = PersonalAccount("John", "Doe", "05210112345")
        assert account.get_birth_year_from_pesel("05210112345") == 2005

    def test_invalid_month(self):
        account = PersonalAccount("John", "Doe", "99130112345")
        assert account.get_birth_year_from_pesel("99130112345") is None

    def test_person_born_after_1960_gets_promo(self):
        account = PersonalAccount("John", "Doe", "64051212345")
        assert account.can_receive_promo("64051212345") is True

    def test_person_born_before_1960_no_promo(self):
        account = PersonalAccount("John", "Doe", "59010112345")
        assert account.can_receive_promo("59010112345") is False

    def test_account_with_promo_and_young_age_gets_promo(self):
        account = PersonalAccount("John", "Doe", "64051212345", promo_code="PROM_XYZ")
        assert account.balance == 50.0

    def test_account_with_promo_and_old_age_gets_no_promo(self):
        account = PersonalAccount("John", "Doe", "59010112345", promo_code="PROM_XYZ")
        assert account.balance == 0.0

    # feature 8
    def test_express_transfer_with_sufficient_balance(self):
        account = PersonalAccount("John", "Doe", "64051212345")
        account.balance = 100.0
        account.outgoing_express_transfer(50.0)
        assert account.balance == 49.0

    def test_express_transfer_allow_negative(self):
        account = PersonalAccount("John", "Doe", "64051212345")
        account.balance = 0.5
        account.outgoing_express_transfer(0.5)
        assert account.balance == -1.0
    
    def test_express_transfer_not_allowed_below_limit(self):
        account = CompanyAccount("MyCompany", "1234567890")
        account.balance = 5.0
        account.outgoing_express_transfer(15.0)
        assert account.balance == 5.0

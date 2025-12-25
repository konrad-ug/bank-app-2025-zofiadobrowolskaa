import unittest
from unittest.mock import patch
from src.company_account import CompanyAccount
import pytest

# mockowanie check_mf dla całej klasy, aby testy nie łączyły się z API
@patch('src.company_account.CompanyAccount.check_mf')
class TestCompanyAccount:
    
    def test_account_creation_valid_nip(self, mock_check):
        mock_check.return_value = True
        account = CompanyAccount("MyCompany", "1234567890")
        assert account.company_name == "MyCompany"
        assert account.nip == "1234567890"
        assert account.balance == 0.0

    def test_too_short_nip(self, mock_check):
        account = CompanyAccount("MyCompany", "123")
        assert account.nip == "Invalid"
    
    def test_too_long_nip(self, mock_check):
        account = CompanyAccount("MyCompany", "12345678901")
        assert account.nip == "Invalid"

    def test_incoming_transfer(self, mock_check):
        mock_check.return_value = True
        account = CompanyAccount("MyCompany", "1234567890")
        account.incoming_transfer(100.0)
        assert account.balance == 100.0

    def test_outgoing_transfer(self, mock_check):
        mock_check.return_value = True
        account = CompanyAccount("MyCompany", "1234567890")
        account.balance = 200.0
        account.outgoing_transfer(50.0)
        assert account.balance == 150.0
    
    def test_express_transfer_company_with_sufficient_balance(self, mock_check):
        mock_check.return_value = True
        account = CompanyAccount("MyCompany", "1234567890")
        account.balance = 100.0
        account.outgoing_express_transfer(50.0)
        assert account.balance == 45.0

    def test_express_transfer_company_allow_negative(self, mock_check):
        mock_check.return_value = True
        account = CompanyAccount("MyCompany", "1234567890")
        account.balance = 2.0
        account.outgoing_express_transfer(2.0)
        assert account.balance == -5.0
    
    def test_express_transfer_company_not_allowed_below_limit(self, mock_check):
        mock_check.return_value = True
        account = CompanyAccount("MyCompany", "1234567890")
        account.balance = 5.0
        account.outgoing_express_transfer(15.0)
        assert account.balance == 5.0

    def test_constructor_raises_error_on_invalid_nip_in_mf(self, mock_check):
        mock_check.return_value = False
        with pytest.raises(ValueError, match="Company not registered!!"):
            CompanyAccount("FraudCorp", "1111111111")
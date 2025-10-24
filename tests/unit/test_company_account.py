from src.company_account import CompanyAccount

class TestCompanyAccount:
    def test_account_creation_valid_nip(self):
        account = CompanyAccount("MyCompany", "1234567890")
        assert account.company_name == "MyCompany"
        assert account.nip == "1234567890"
        assert account.balance == 0.0

    def test_too_short_nip(self):
        account = CompanyAccount("MyCompany", "123")
        assert account.nip == "Invalid"
    
    def test_too_long_nip(self):
        account = CompanyAccount("MyCompany", "12345678901")
        assert account.nip == "Invalid"

    def test_incoming_transfer(self):
        account = CompanyAccount("MyCompany", "1234567890")
        account.incoming_transfer(100.0)
        assert account.balance == 100.0

    def test_outgoing_transfer(self):
        account = CompanyAccount("MyCompany", "1234567890")
        account.balance = 200.0
        account.outgoing_transfer(50.0)
        assert account.balance == 150.0

from src.accounts_registry import AccountsRegistry
from src.personal_account import PersonalAccount
import pytest

@pytest.fixture()
def registry():
    return AccountsRegistry()


class TestAccountsRegistry:
    @pytest.mark.parametrize("first_name, last_name, pesel",
    [
        ("Jan", "Kowalski", "64051212345"),
        ("Anna", "Nowak", "05210112345"),
        ("Piotr", "Zieliński", "59010112345")
    ]
    )
    def test_accounts_registry(self, registry, first_name, last_name, pesel):
        account = PersonalAccount(first_name, last_name, pesel)
        
        registry.add_account(account)
        found = registry.find_by_pesel(pesel)
        assert found == account

        assert registry.get_accounts_count() == 1

        all_accounts = registry.return_accounts()
        assert len(all_accounts) == 1
    
    def test_find_by_pesel_not_found(self, registry):
        result = registry.find_by_pesel("00000000000")
        assert result is None
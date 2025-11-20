import pytest
from src.company_account import CompanyAccount

@pytest.fixture()
def company():
    return CompanyAccount("MyCompany", "1234567890")

class TestCompanyLoan:

    @pytest.mark.parametrize(
        "balance, history, loan_amount, expected_result, expected_balance",
        [
            (5000, [-100, -1775, 3000], 1000, True, 6000),
            (6000, [-100, -200, -50], 1000, False, 6000),
            (1500, [-1775], 1000, False, 1500),
            (2000, [-20, -1775], 1000, True, 3000),
            (4000, [], 1000, False, 4000),
            (8000, [-1775, -500, -1775], 2000, True, 10000),
            (20000, [-50, -1775], 9000, True, 29000),
        ],
        ids=[
            "loan_granted_2_conditions",
            "no_zus_payment",
            "insufficient_balance",
            "loan_granted_exact_balance",
            "empty_history",
            "multiple_zus_payments",
            "large_loan_granted",
        ]
    )
    def test_take_loan(self, company, balance, history, loan_amount, expected_result, expected_balance):
        company.balance = balance
        company.history = history
        result = company.take_loan(loan_amount)

        assert result == expected_result
        assert company.balance == expected_balance

        if expected_result:
            assert company.history[-1] == loan_amount
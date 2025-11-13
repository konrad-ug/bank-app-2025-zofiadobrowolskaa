import pytest
from src.personal_account import PersonalAccount

@pytest.fixture()
def account():
    return PersonalAccount("John", "Doe", "64051212345")


class TestLoan:

    @pytest.mark.parametrize("history, loan_amount, expected_result, expected_balance",
        [
            ([-30, -10, 300, 10, 30], 200, True, 200),
            ([5, -1, 40, 50], 300, False, 0),
            ([12, -4, 50, 100, 10], 150, True, 150),
            ([12, -4, 50, 100, 10], 100, True, 100),
            ([-2, 100, 50], 30, False, 0),
            ([500, -100, 200, -50, 600], 1000, True, 1000)
        ],
        ids=[
            "loan_granted_last_three_positive",
            "loan_denied_last_three_not_all_positive",
            "loan_granted_sum_last_five_greater",
            "loan_granted_sum_last_five_greater_edge",
            "loan_denied_not_enough_transactions",
            "loan_granted_sum_last_five_with_negatives"
        ]
    )
    def test_submit_for_loan(self, account, history, loan_amount, expected_result, expected_balance):
        account.history = history
        result = account.submit_for_loan(loan_amount)
        assert result == expected_result
        assert account.balance == expected_balance
        if expected_result:
            assert account.history[-1] == expected_balance

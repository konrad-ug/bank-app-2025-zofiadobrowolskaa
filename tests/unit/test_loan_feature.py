from src.personal_account import PersonalAccount

class TestLoanFeature:
    def test_loan_granted_when_last_three_positive(self):
        account = PersonalAccount("John", "Doe", "64051212345")
        account.history = [-30.0, -10.0, 300, 10, 30]
        result = account.submit_for_loan(200.0)
        assert result is True
        assert account.balance == 200.0
        assert account.history[-1] == 200.0
    
    def test_loan_denied_when_last_three_not_all_positive(self):
        account = PersonalAccount("John", "Doe", "64051212345")
        account.history = [5.0, -1.0, 40.0, 50.0]
        result = account.submit_for_loan(300.0)
        assert result is False
        assert account.balance == 0.0
        assert account.history == [5.0, -1.0, 40.0, 50.0]
    
    def test_loan_granted_when_sum_of_last_five_is_greater_than_amount(self):
        account = PersonalAccount("John", "Doe", "64051212345")
        account.history = [12.0, -4.0, 50.0, 100.0, 10.0]
        result = account.submit_for_loan(150.0)
        assert result is True
        assert account.balance == 150.0
        assert account.history[-1] == 150.0
    
    def test_loan_denied_when_sum_of_last_five_is_not_greater_than_amount(self):
        account = PersonalAccount("John", "Doe", "64051212345")
        account.history = [12.0, -4.0, 50.0, 100.0, 10.0]
        result = account.submit_for_loan(100.0)
        assert result is True
        assert account.balance == 100.0
        assert account.history[-1] == 100.0

    
    def test_loan_denied_when_not_enough_transactions(self):
        account = PersonalAccount("John", "Doe", "64051212345")
        account.history = [-2.0, 100.0, 50.0]
        result = account.submit_for_loan(30.0)
        assert result is False
        assert account.balance == 0.0
    
    def test_loan_granted_by_second_condition_even_with_negatives(self):
        account = PersonalAccount("John", "Doe", "64051212345")
        account.history = [500.0, -100.0, 200.0, -50.0, 600.0]
        result = account.submit_for_loan(1000.0)
        assert result is True
        assert account.balance == 1000.0
        assert account.history[-1] == 1000.0

    




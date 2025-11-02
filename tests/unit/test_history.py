from src.account import Account
from src.personal_account import PersonalAccount

class TestHistory:
    def test_incoming_transfer_adds_to_history(self):
        account = Account()
        account.incoming_transfer(100)
        assert account.history == [100.0]

    def test_outgoing_transfer_adds_negative_to_history(self):
        account = Account()
        account.balance = 200
        account.outgoing_transfer(100)
        assert account.history == [ -100.0 ]

    def test_outgoing_express_transfer_history(self):
        account = PersonalAccount("John", "Doe", "64051212345")
        account.balance = 500
        account.outgoing_express_transfer(300)
        assert account.history == [-300.0, -1.0]
    
    def test_incoming_and_express_transfer_history(self):
        account = PersonalAccount("John", "Doe", "64051212345")
        account.incoming_transfer(500)
        account.balance = 500
        account.outgoing_express_transfer(300)
        assert account.history == [500.0, -300.0, -1.00]

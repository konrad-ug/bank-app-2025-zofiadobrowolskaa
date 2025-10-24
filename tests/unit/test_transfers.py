from src.account import Account

# feature 6
class TestTransfers:
    def test_incoming_transfer(self):
        account = Account("John", "Doe", "05290706768")
        account.incoming_transfer(100.0)
        assert account.balance == 100.0
    
    def test_outgoing_transfer(self):
        account = Account("John", "Doe", "05290706768")
        account.balance = 200.0 # 1. set up

        account.outgoing_transfer(50.0) #2. action
        assert account.balance == 150.0 #3. assertion
    
    def test_transfer_insufficient_funds(self):
        account = Account("John", "Doe", "05290706768")
        account.outgoing_transfer(30.0)
        assert account.balance == 0.0
    
    def test_incoming_negative_transfer(self):
        account = Account("John", "Doe", "05290706768")
        account.incoming_transfer(-20.0)
        assert account.balance == 0.0
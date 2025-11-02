class Account:
    def __init__(self, first_name=None, last_name=None, pesel=None):
        self.balance = 0.0

    
    def incoming_transfer(self, amount: float):
        if amount > 0:
            self.balance += amount
    
    def outgoing_transfer(self, amount: float):
        if 0 < amount <= self.balance:
            self.balance -= amount
    
    def temp_method(self):
        return True

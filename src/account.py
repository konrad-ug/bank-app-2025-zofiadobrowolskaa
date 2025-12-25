from datetime import date
from src.smtp.smtp import SMTPClient

class Account:
    def __init__(self, first_name=None, last_name=None, pesel=None):
        self.balance = 0.0
        self.history = []

    
    def incoming_transfer(self, amount: float):
        if amount > 0:
            self.balance += amount
            self.history.append(amount)
    
    def outgoing_transfer(self, amount: float):
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.history.append(-amount)
            return True
        return False
    
    def send_history_via_email(self, email_address):
        today = date.today().strftime("%Y-%m-%d")
        subject = f"Account Transfer History {today}"
        
        prefix = "Personal account history" if self.__class__.__name__ == "PersonalAccount" else "Company account history"
        content = f"{prefix}:{self.history}"
        
        client = SMTPClient()
        return client.send(subject, content, email_address)

    

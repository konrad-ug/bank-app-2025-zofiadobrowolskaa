from src.account import Account

class CompanyAccount(Account):
    def __init__(self, company_name, nip):
        super().__init__() # dzieki temu moge odziedziczyc saldo i obslugiwac przelewy
        self.company_name = company_name
        self.nip = nip if self.is_nip_valid(nip) else 'Invalid'

    def is_nip_valid(self, nip):
        return isinstance(nip, str) and len(nip) == 10 and nip.isdigit()
    
    def outgoing_express_transfer(self, amount):
        fee = 5.0
        max_overdraft = fee # saldo może zejść poniżej 0 maksymalnie o kwotę opłaty

        if self.balance - amount - fee < -max_overdraft:
            return self.balance
        
        self.balance -= amount + fee
        self.history.append(-amount)
        self.history.append(-fee)
        return self.balance
    
    def take_loan(self, amount):
        if self.balance < 2 * amount:
            return False
        
        if -1775 not in self.history:
            return False
        
        self.balance += amount
        self.history.append(amount)
        return True

    
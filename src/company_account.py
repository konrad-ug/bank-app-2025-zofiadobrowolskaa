from src.account import Account

class CompanyAccount(Account):
    def __init__(self, company_name, nip):
        super().__init__() # dzieki temu moge odziedziczyc saldo i obslugiwac przelewy
        self.company_name = company_name
        self.nip = nip if self.is_nip_valid(nip) else 'Invalid'

    def is_nip_valid(self, nip):
        return isinstance(nip, str) and len(nip) == 10 and nip.isdigit()

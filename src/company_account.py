import os
import requests
from datetime import date
from src.account import Account

class CompanyAccount(Account):
    def __init__(self, company_name, nip):
        super().__init__() # dzieki temu moge odziedziczyc saldo i obslugiwac przelewy
        self.company_name = company_name

        if not self.is_nip_valid(nip):
            self.nip = 'Invalid'
        else:
            if self.check_mf(nip):
                self.nip = nip
            else:
                raise ValueError("Company not registered!!")

    def is_nip_valid(self, nip):
        return isinstance(nip, str) and len(nip) == 10 and nip.isdigit()

    def check_mf(self, nip):
        url_mf = os.getenv('BANK_APP_MF_URL', 'https://wl-test.mf.gov.pl')
        today = date.today().strftime("%Y-%m-%d")
        
        url = f"{url_mf}/api/search/nip/{nip}?date={today}"
        
        res = requests.get(url)
        data = res.json()
        
        print(f"MF Response: {data}")

        try:
            info = data.get("result", {}).get("subject", {})
            if info and info.get("statusVat") == "Czynny":
                return True
        except:
            pass
            
        return False
        
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

    
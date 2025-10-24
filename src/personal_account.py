from src.account import Account

class PersonalAccount(Account):
    def __init__(self, first_name, last_name, pesel, promo_code=None):
        super().__init__() # dzieki temu moge odziedziczyc saldo i obslugiwac przelewy
        self.first_name = first_name
        self.last_name = last_name
        self.pesel = pesel if self.is_pesel_valid(pesel) else 'Invalid'
        self.balance = 50.0 if self.is_promo_code_valid(promo_code) and self.can_receive_promo(pesel) else 0.0

    def is_pesel_valid(self, pesel):
        return isinstance(pesel, str) and len(pesel) == 11 and pesel.isdigit()

    def is_promo_code_valid(self, promo_code):
        if not isinstance(promo_code, str):
            return False
        return promo_code.startswith("PROM_") and len(promo_code) == 8

    def get_birth_year_from_pesel(self, pesel):
        if not self.is_pesel_valid(pesel):
            return None

        year = int(pesel[0:2])
        month = int(pesel[2:4])

        if 1 <= month <= 12:
            year += 1900
        elif 21 <= month <= 32:
            year += 2000
        elif 81 <= month <= 92:
            year += 1800
        else:
            return None
        
        return year

    def can_receive_promo(self, pesel):
        year = self.get_birth_year_from_pesel(pesel)
        if year is None:
            return False
        return year > 1960
    
    def outgoing_express_transfer(self, amount):
        fee = 1.0
        max_overdraft = fee # saldo może zejść poniżej 0 maksymalnie o kwotę opłaty

        if self.balance - amount - fee < -max_overdraft:
            return self.balance
        
        self.balance -= amount + fee
        return self.balance

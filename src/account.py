class Account:
    def __init__(self, first_name, last_name, pesel, promo_code=None):
        self.first_name = first_name
        self.last_name = last_name
        self.balance = 0.0
        self.pesel = pesel if self.is_pesel_valid(pesel) else 'Invalid'

        if self.is_promo_code_valid(promo_code):
            self.balance += 50

    def is_pesel_valid(self, pesel):
        return isinstance(pesel, str) and len(pesel) == 11

    def is_promo_code_valid(self, promo_code):
        if not isinstance(promo_code, str):
            return False
        return promo_code.startswith("PROM_") and len(promo_code) == 8

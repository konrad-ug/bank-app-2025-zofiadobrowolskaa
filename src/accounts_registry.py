from src.personal_account import PersonalAccount

class AccountsRegistry:
    def __init__(self):
        self.accounts = []

    def add_account(self, account: PersonalAccount):
        self.accounts.append(account)

    def find_by_pesel(self, pesel):
        for account in self.accounts:
            if account.pesel == pesel:
                return account
            
        return None
    
    def return_accounts(self):
        return self.accounts
    
    def get_accounts_count(self):
        return len(self.accounts)
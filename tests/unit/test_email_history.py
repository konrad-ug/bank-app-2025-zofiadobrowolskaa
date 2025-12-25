import unittest
from unittest.mock import patch, MagicMock
from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount
from datetime import date

class TestEmailHistory(unittest.TestCase):
    def setUp(self):
        self.address = "test@email.com"
        self.today = date.today().strftime("%Y-%m-%d")

    @patch('src.smtp.smtp.SMTPClient.send')
    def test_send_history_personal_account_success(self, mock_send):
        mock_send.return_value = True
        
        account = PersonalAccount("John", "Doe", "64051212345")
        account.history = [100, -50]
        
        result = account.send_history_via_email(self.address)
        
        self.assertTrue(result)

        mock_send.assert_called_once()
      
        args, kwargs = mock_send.call_args
        self.assertEqual(args[0], f"Account Transfer History {self.today}")
        self.assertEqual(args[1], "Personal account history:[100, -50]")
        self.assertEqual(args[2], self.address)

    @patch('src.smtp.smtp.SMTPClient.send')
    @patch('src.company_account.CompanyAccount.check_mf')
    def test_send_history_company_account_failure(self, mock_mf, mock_send):
        mock_mf.return_value = True
        mock_send.return_value = False
        
        company = CompanyAccount("MyCompany", "1234567890")
        company.history = [500, -100]
        
        result = company.send_history_via_email(self.address)
        
        self.assertFalse(result)
        mock_send.assert_called_once()
        
        args = mock_send.call_args[0]
        self.assertEqual(args[1], "Company account history:[500, -100]")

    @patch('src.smtp.smtp.SMTPClient.send')
    def test_send_history_empty_history(self, mock_send):
        mock_send.return_value = True
        account = PersonalAccount("John", "Doe", "64051212345")
        account.send_history_via_email(self.address)
        
        args = mock_send.call_args[0]
        self.assertEqual(args[1], "Personal account history:[]")
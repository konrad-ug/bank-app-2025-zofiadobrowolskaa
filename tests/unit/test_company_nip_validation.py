import unittest
from unittest.mock import patch
from src.company_account import CompanyAccount

class TestCompanyNipValidation(unittest.TestCase):
    name = "My Company"
    nip = "8461627563"

    @patch('requests.get')
    def test_create_company_success(self, mock_get):
        mock_get.return_value.json.return_value = {
            "result": {
                "subject": {"statusVat": "Czynny"}
            }
        }
        mock_get.return_value.status_code = 200

        account = CompanyAccount(self.name, self.nip)
        self.assertEqual(account.nip, self.nip)
        self.assertEqual(account.company_name, self.name)

    @patch('requests.get')
    def test_create_company_not_active(self, mock_get):
        mock_get.return_value.json.return_value = {
            "result": {
                "subject": {"statusVat": "Zwolniony"}
            }
        }
        
        with self.assertRaises(ValueError) as context:
            CompanyAccount(self.name, self.nip)
        
        self.assertTrue("Company not registered!!" in str(context.exception))

    @patch('requests.get')
    def test_create_company_invalid_nip_format(self, mock_get):
        invalid_nip = "123"
        account = CompanyAccount(self.name, invalid_nip)
        
        self.assertEqual(account.nip, "Invalid")
        mock_get.assert_not_called()
    
    @patch('requests.get')
    def test_create_company_api_error(self, mock_get):
        mock_get.return_value.json.return_value = {}
        
        with self.assertRaises(ValueError):
            CompanyAccount(self.name, self.nip)
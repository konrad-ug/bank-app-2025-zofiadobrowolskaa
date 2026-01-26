import unittest
from unittest.mock import MagicMock, patch
from src.mongo_accounts_repository import MongoAccountsRepository
from src.personal_account import PersonalAccount

class TestMongoAccountsRepository(unittest.TestCase):
    
    @patch('src.mongo_accounts_repository.MongoClient')
    def setUp(self, mock_client):
        self.mock_client = mock_client
        self.repo = MongoAccountsRepository()
        self.mock_collection = self.repo.collection

    def test_save_all(self):
        account = PersonalAccount("Jan", "Kowalski", "12345678901")
        accounts = [account]

        self.repo.save_all(accounts)

        self.mock_collection.delete_many.assert_called_once_with({})
        self.mock_collection.insert_many.assert_called_once()
        
    def test_load_all(self):
        mock_data = [{
            "type": "personal",
            "first_name": "Jan",
            "last_name": "Kowalski",
            "pesel": "12345678901",
            "balance": 100.0,
            "history": [100.0]
        }]
        self.mock_collection.find.return_value = mock_data

        loaded_accounts = self.repo.load_all()

        self.assertEqual(len(loaded_accounts), 1)
        self.assertIsInstance(loaded_accounts[0], PersonalAccount)
        self.assertEqual(loaded_accounts[0].balance, 100.0)
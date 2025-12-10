import pytest
import requests

class TestAccountAPI:
    url = "http://127.0.0.1:5000/api/accounts"
    account_details = {
        "name": "John",
        "surname": "Doe",
        "pesel": "12345678901"
    }

    @pytest.fixture(autouse=True)
    def set_up(self):
        response = requests.post(self.url, json=self.account_details)
        assert response.status_code == 201
        yield
       
        accounts = requests.get(self.url).json()
        for account in accounts:
            del_res = requests.delete(f"{self.url}/{account['pesel']}")
            assert del_res.status_code == 200

    def test_create_account(self):
        account = {"name": "Alice", "surname": "Smith", "pesel": "09876543210"}
        response = requests.post(self.url, json=account)
        assert response.status_code == 201
        assert response.json()["message"] == "Account created"

    def test_get_account_by_pesel(self):
        response = requests.get(f"{self.url}/{self.account_details['pesel']}")
        assert response.status_code == 200
        data = response.json()
        assert data["pesel"] == self.account_details["pesel"]
        assert data["name"] == self.account_details["name"]
        assert data["surname"] == self.account_details["surname"]

    def test_get_account_not_found(self):
        response = requests.get(f"{self.url}/00000000000")
        assert response.status_code == 404
        assert response.json()["message"] == "Account not found"

    def test_update_account(self):
        update_data = {"name": "Bob", "surname": "Williams"}
        response = requests.patch(f"{self.url}/{self.account_details['pesel']}", json=update_data)
        assert response.status_code == 200
        assert response.json()["message"] == "Account updated"

        get_res = requests.get(f"{self.url}/{self.account_details['pesel']}")
        data = get_res.json()
        assert data["name"] == "Bob"
        assert data["surname"] == "Williams"

    def test_delete_account(self):
        response = requests.delete(f"{self.url}/{self.account_details['pesel']}")
        assert response.status_code == 200
        assert response.json()["message"] == "Account deleted"

        get_res = requests.get(f"{self.url}/{self.account_details['pesel']}")
        assert get_res.status_code == 404
    
    def test_create_account_with_existing_pesel(self):
        duplicate_account = {
            "name": "Duplicate",
            "surname": "User",
            "pesel": self.account_details["pesel"]
        }
        response = requests.post(self.url, json=duplicate_account)
        assert response.status_code == 409
        assert response.json()["message"] == "Account with this PESEL already exists"

    def test_incoming_transfer(self):
        transfer_data = {"amount": 500, "type": "incoming"}
        response = requests.post(f"{self.url}/{self.account_details['pesel']}/transfer", json=transfer_data)
        assert response.status_code == 200
        assert response.json()["message"] == "Transfer successful"

    def test_outgoing_transfer_success(self):
        requests.post(f"{self.url}/{self.account_details['pesel']}/transfer", json={"amount": 1000, "type": "incoming"})
        
        transfer_data = {"amount": 500, "type": "outgoing"}
        response = requests.post(f"{self.url}/{self.account_details['pesel']}/transfer", json=transfer_data)
        assert response.status_code == 200
        assert response.json()["message"] == "Transfer successful"

    def test_outgoing_transfer_failure(self):
        transfer_data = {"amount": 5000, "type": "outgoing"}
        response = requests.post(f"{self.url}/{self.account_details['pesel']}/transfer", json=transfer_data)
        assert response.status_code == 422
        assert response.json()["message"] == "Insufficient funds"

    def test_transfer_unknown_account(self):
        transfer_data = {"amount": 100, "type": "incoming"}
        response = requests.post(f"{self.url}/0000000/transfer", json=transfer_data)
        assert response.status_code == 404
        assert response.json()["message"] == "Account not found"

    def test_transfer_unknown_type(self):
        transfer_data = {"amount": 100, "type": "invalid"}
        response = requests.post(f"{self.url}/{self.account_details['pesel']}/transfer", json=transfer_data)
        assert response.status_code == 400
        assert response.json()["message"] == "Unknown transfer type"

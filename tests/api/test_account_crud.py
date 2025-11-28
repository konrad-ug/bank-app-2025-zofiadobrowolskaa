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

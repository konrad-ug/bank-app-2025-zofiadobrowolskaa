import pytest
import requests

url = "http://127.0.0.1:5000/api/accounts"

@pytest.fixture
def sample_account():
    account = {"name": "John", "surname": "Doe", "pesel": "12345678901"}
    requests.post(url, json=account)
    return account

def test_sample_account():
    account = {"name": "Alice", "surname": "Smith", "pesel": "09876543210"}
    response = requests.post(url, json=account)
    assert response.status_code == 201
    assert response.json()["message"] == "Account created"

def test_get_account_by_pesel(sample_account):
    response = requests.get(f"{url}/{sample_account["pesel"]}")
    assert response.status_code == 200
    data = response.json()
    assert data["pesel"] == sample_account["pesel"]
    assert data["name"] == sample_account["name"]

def test_get_account_not_found():
    response = requests.get(f"{url}/11111111111")
    assert response.status_code == 404
    assert response.json()["message"] == "Account not found"

def test_update_account(sample_account):
    update_data = {"name": "Bob", "surname": "Williams"}
    response = requests.patch(f"{url}/{sample_account["pesel"]}", json=update_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Account updated"

def test_delete_account(sample_account):
    response = requests.delete(f"{url}/{sample_account["pesel"]}")
    assert response.status_code == 200
    assert response.json()["message"] == "Account deleted"
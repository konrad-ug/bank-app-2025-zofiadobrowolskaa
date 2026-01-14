import pytest
import requests

class TestPerf:
    body = {
        "name": "John",
        "surname": "Doe",
        "pesel": "12345678901"
    }
    url = "http://127.0.0.1:5000/api/accounts"
    iteration_count = 100
    timeout = 0.5

    @pytest.fixture(autouse=True, scope="function")
    def clear(self):
        try:
            response = requests.get(self.url, timeout=self.timeout)
            if response.status_code == 200:
                accounts = response.json()
                for account in accounts:
                    pesel = account['pesel']
                    requests.delete(f"{self.url}/{pesel}", timeout=self.timeout)
        except Exception:
            pass

    def test_create_delete_perf_test(self):
        for _ in range(self.iteration_count):
            create_response = requests.post(self.url, json=self.body, timeout=self.timeout)
            assert create_response.status_code == 201
            
            delete_response = requests.delete(f"{self.url}/{self.body['pesel']}", timeout=self.timeout)
            assert delete_response.status_code == 200
    
    def test_create_delete_perf_group(self):
        pesels = [f"1234567{i:04d}" for i in range(1000)]
        for pesel in pesels:
            body = {**self.body, "pesel": pesel}
            create_response = requests.post(self.url, json=body, timeout=self.timeout)
            assert create_response.status_code == 201
        for pesel in pesels:
            delete_response = requests.delete(f"{self.url}/{pesel}", timeout=self.timeout)
            assert delete_response.status_code == 200

    def test_transfer_perf(self):
        create_response = requests.post(self.url, json=self.body, timeout=self.timeout)
        assert create_response.status_code == 201
        
        for _ in range(self.iteration_count):
            transfer_response = requests.post(f"{self.url}/{self.body['pesel']}/transfer", json={
                "type": "incoming",
                "amount": 100
            }, timeout=self.timeout)
            assert transfer_response.status_code == 200
        
        account = requests.get(f"{self.url}/{self.body['pesel']}", timeout=self.timeout)
        assert account.json()['balance'] == 100 * self.iteration_count
        
        delete_response = requests.delete(f"{self.url}/{self.body['pesel']}", timeout=self.timeout)
        assert delete_response.status_code == 200
import requests
from data.urls import Urls


class UserApi:
    def __init__(self, base_url=Urls.API_BASE_URL):
        self.base_url = base_url.rstrip("/")

    def register(self, email, password, name):
        resp = requests.post(
            f"{self.base_url}/auth/register",
            json={"email": email, "password": password, "name": name},
            timeout=10,
        )
        return resp

    def login(self, email, password):
        resp = requests.post(
            f"{self.base_url}/auth/login",
            json={"email": email, "password": password},
            timeout=10,
        )
        return resp

    def delete(self, access_token):
        resp = requests.delete(
            f"{self.base_url}/auth/user",
            headers={"Authorization": access_token},
            timeout=10,
        )
        return resp
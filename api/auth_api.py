import requests

from api.base_client import BaseClient
from wrappers import api_logger


class AuthApi:

    def __init__(self, client: BaseClient):
        self._client = client

    @api_logger("POST /auth/login")
    def login(self, username: str, password: str) -> requests.Response:
        return self._client.post(
            "/auth/login",
            json={"username": username, "password": password, "expiresInMins": 30},
        )

    @api_logger("POST /auth/refresh")
    def refresh(self, refresh_token: str) -> requests.Response:
        # refresh_token goes in body, not in Authorization header
        return self._client.request_no_auth(
            "POST", "/auth/refresh",
            json={"refreshToken": refresh_token, "expiresInMins": 30},
        )

    @api_logger("GET /auth/me")
    def get_me(self) -> requests.Response:
        return self._client.get("/auth/me")

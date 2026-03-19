from urllib.parse import urljoin

import requests

from utils.config import settings


class BaseClient:

    def __init__(self, base_url: str = None):
        self.base_url = base_url or settings.BASE_URL
        self.session = requests.Session()
        self._token_type: str = None
        self._auth_token: str = None

    def set_headers(self, headers: dict):
        self.session.headers.clear()
        self.session.headers.update(headers)

    def set_auth_token(self, token_type: str, token: str):
        self._token_type = token_type
        self._auth_token = token
        self.session.headers["Authorization"] = f"{token_type} {token}"

    def clear_auth(self):
        self._auth_token = None
        self._token_type = None
        self.session.headers.pop("Authorization", None)

    @property
    def is_authenticated(self) -> bool:
        return self._auth_token is not None

    @property
    def authorization(self) -> str | None:
        return self._auth_token

    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        kwargs.setdefault("timeout", settings.DEFAULT_TIMEOUT)
        url = urljoin(self.base_url, path)
        return self.session.request(method, url, **kwargs)

    def request_no_auth(self, method: str, path: str, **kwargs) -> requests.Response:
        kwargs.setdefault("timeout", settings.DEFAULT_TIMEOUT)
        url = urljoin(self.base_url, path)
        auth_header = self.session.headers.pop("Authorization", None)
        try:
            return self.session.request(method, url, **kwargs)
        finally:
            if auth_header:
                self.session.headers["Authorization"] = auth_header

    def get(self, path: str, **kwargs) -> requests.Response:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs) -> requests.Response:
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs) -> requests.Response:
        return self.request("PUT", path, **kwargs)

    def patch(self, path: str, **kwargs) -> requests.Response:
        return self.request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs) -> requests.Response:
        return self.request("DELETE", path, **kwargs)

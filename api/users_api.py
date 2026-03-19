import requests

from api.base_client import BaseClient
from wrappers import api_logger


class UsersApi:

    def __init__(self, client: BaseClient):
        self._client = client

    @api_logger("GET /users")
    def get_users(self, limit: int = 10, skip: int = 0) -> requests.Response:
        return self._client.get("/users", params={"limit": limit, "skip": skip})

    @api_logger("GET /users/{id}")
    def get_user(self, user_id: int) -> requests.Response:
        return self._client.get(f"/users/{user_id}")

    @api_logger("GET /users/search")
    def search_users(self, query: str) -> requests.Response:
        return self._client.get("/users/search", params={"q": query})

    @api_logger("POST /users/add")
    def create_user(self, first_name: str, last_name: str, age: int) -> requests.Response:
        return self._client.post(
            "/users/add",
            json={"firstName": first_name, "lastName": last_name, "age": age},
        )

    @api_logger("PUT /users/{id}")
    def update_user(self, user_id: int, **fields) -> requests.Response:
        return self._client.put(f"/users/{user_id}", json=fields)

    @api_logger("DELETE /users/{id}")
    def delete_user(self, user_id: int) -> requests.Response:
        return self._client.delete(f"/users/{user_id}")

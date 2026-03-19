from api.auth_api import AuthApi
from api.base_client import BaseClient
from api.products_api import ProductsApi
from api.users_api import UsersApi


class ApiFacade:

    def __init__(self, client: BaseClient):
        self._client = client
        self._client.set_headers({
            "Accept": "application/json",
            "Content-Type": "application/json",
        })
        self._auth: AuthApi = None
        self._users: UsersApi = None
        self._products: ProductsApi = None

    def set_auth_token(self, token_type: str, token: str):
        self._client.set_auth_token(token_type, token)

    def clear_auth(self):
        self._client.clear_auth()

    @property
    def is_authenticated(self) -> bool:
        return self._client.is_authenticated

    @property
    def authorization(self) -> str | None:
        return self._client.authorization

    @property
    def auth(self) -> AuthApi:
        if self._auth is None:
            self._auth = AuthApi(self._client)
        return self._auth

    @property
    def users(self) -> UsersApi:
        if self._users is None:
            self._users = UsersApi(self._client)
        return self._users

    @property
    def products(self) -> ProductsApi:
        if self._products is None:
            self._products = ProductsApi(self._client)
        return self._products

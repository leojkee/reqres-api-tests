import requests

from api.base_client import BaseClient
from wrappers import api_logger


class ProductsApi:

    def __init__(self, client: BaseClient):
        self._client = client

    @api_logger("GET /products")
    def get_products(self, limit: int = 10, skip: int = 0) -> requests.Response:
        return self._client.get("/products", params={"limit": limit, "skip": skip})

    @api_logger("GET /products/{id}")
    def get_product(self, product_id: int) -> requests.Response:
        return self._client.get(f"/products/{product_id}")

    @api_logger("GET /products/search")
    def search_products(self, query: str) -> requests.Response:
        return self._client.get("/products/search", params={"q": query})

    @api_logger("POST /products/add")
    def create_product(self, title: str, price: float, category: str) -> requests.Response:
        return self._client.post(
            "/products/add",
            json={"title": title, "price": price, "category": category},
        )

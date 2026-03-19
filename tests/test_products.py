import allure
import pytest

from api.api_facade import ApiFacade
from model.product_model import ProductListResponse, ProductData, CreateProductResponse


@allure.feature("Products")
@allure.story("Read & Create")
@allure.severity(allure.severity_level.NORMAL)
class TestProducts:

    @pytest.mark.smoke
    @pytest.mark.regression
    @allure.title("Get products list")
    def test_get_products(self, api: ApiFacade):
        response = api.products.get_products(limit=5)
        assert response.status_code == 200
        data = ProductListResponse(**response.json())
        assert len(data.products) == 5
        assert data.total > 0

    @pytest.mark.regression
    @pytest.mark.parametrize("limit", [5, 10, 20])
    @allure.title("Get products — various limits")
    def test_get_products_limits(self, api: ApiFacade, limit: int):
        response = api.products.get_products(limit=limit)
        assert response.status_code == 200
        data = response.json()
        assert data["limit"] == limit

    @pytest.mark.smoke
    @pytest.mark.regression
    @allure.title("Get single product by ID")
    def test_get_single_product(self, api: ApiFacade):
        response = api.products.get_product(1)
        assert response.status_code == 200
        ProductData(**response.json())
        assert response.json()["id"] == 1

    @pytest.mark.regression
    @allure.title("Get non-existent product — 404")
    def test_get_product_not_found(self, api: ApiFacade):
        response = api.products.get_product(9999)
        assert response.status_code == 404

    @pytest.mark.regression
    @allure.title("Search products")
    def test_search_products(self, api: ApiFacade):
        response = api.products.search_products("phone")
        assert response.status_code == 200
        data = ProductListResponse(**response.json())
        assert len(data.products) > 0

    @pytest.mark.regression
    @allure.title("Create product")
    def test_create_product(self, api: ApiFacade):
        response = api.products.create_product(
            title="Test Laptop",
            price=999.99,
            category="laptops",
        )
        assert response.status_code == 201
        data = CreateProductResponse(**response.json())
        assert data.title == "Test Laptop"
        assert data.price == 999.99

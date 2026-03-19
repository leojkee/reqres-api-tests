import allure
import pytest


@pytest.fixture(autouse=True)
def _allure_test_info(request):
    allure.dynamic.parameter("test_id", request.node.nodeid)
    yield

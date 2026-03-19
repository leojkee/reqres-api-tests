import pytest

from api.admin.admin_api_facade import AdminApiFacade
from api.api_facade import ApiFacade
from api.base_client import BaseClient
from utils.config import settings
from utils.test_context import set_test_id, clear_test_id


@pytest.fixture(autouse=True)
def _set_test_context(request):
    nodeid = request.node.nodeid.split("[")[0]
    set_test_id(nodeid)
    yield
    clear_test_id()


@pytest.fixture(scope="function")
def api() -> ApiFacade:
    return ApiFacade(BaseClient())


@pytest.fixture(scope="session")
def admin_api() -> AdminApiFacade:
    return AdminApiFacade(BaseClient())


@pytest.fixture(scope="function")
def admin_api_authenticated(admin_api: AdminApiFacade) -> AdminApiFacade:
    response = admin_api.auth.login(settings.ADMIN_USERNAME, settings.ADMIN_PASSWORD)
    data = response.json()
    admin_api.set_auth_token("Bearer", data["accessToken"])
    return admin_api

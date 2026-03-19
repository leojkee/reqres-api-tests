import allure
import pytest

from api.api_facade import ApiFacade
from steps.auth_steps import login_flow, login_and_refresh_flow, login_invalid_flow
from utils.config import settings


@allure.feature("Auth")
@allure.story("Login & Token")
@allure.severity(allure.severity_level.CRITICAL)
class TestAuth:

    @pytest.mark.smoke
    @pytest.mark.regression
    @allure.title("Successful login and profile fetch")
    @allure.description("""
    Verifies the full login -> /auth/me flow.

    Steps:
    1. Login with valid credentials.
    2. Fetch current user profile via /auth/me.

    Expected result:
    - Access token returned.
    - Profile email matches.
    """)
    def test_login_and_get_profile(self, api: ApiFacade):
        flow = login_flow(
            username=settings.TEST_USERNAME,
            password=settings.TEST_PASSWORD,
            api=api,
        )
        assert flow["login"]["accessToken"]
        assert flow["me"]["username"] == settings.TEST_USERNAME
        assert api.is_authenticated

    @pytest.mark.smoke
    @pytest.mark.regression
    @allure.title("Login and refresh token")
    @allure.description("""
    Verifies token refresh flow.

    Steps:
    1. Login with valid credentials.
    2. Use refreshToken to get new accessToken.

    Expected result:
    - New accessToken is returned.
    """)
    def test_login_and_refresh_token(self, api: ApiFacade):
        flow = login_and_refresh_flow(
            username=settings.TEST_USERNAME,
            password=settings.TEST_PASSWORD,
            api=api,
        )
        assert flow["login"]["accessToken"]
        assert flow["refresh"]["accessToken"]
        assert flow["refresh"]["refreshToken"]




    @pytest.mark.regression
    @allure.title("Login with wrong password — 400")
    def test_login_wrong_password(self, api: ApiFacade):
        flow = login_invalid_flow(
            username=settings.TEST_USERNAME,
            password="wrongpassword",
            api=api,
        )
        assert flow["login"]["status_code"] == 400

    @pytest.mark.regression
    @allure.title("Login with non-existent user — 400")
    def test_login_unknown_user(self, api: ApiFacade):
        flow = login_invalid_flow(
            username="nonexistent_user_xyz",
            password="anypassword",
            api=api,
        )
        assert flow["login"]["status_code"] == 400

    @pytest.mark.regression
    @allure.title("Get /auth/me without token — 401")
    def test_get_me_unauthenticated(self, api: ApiFacade):
        response = api.auth.get_me()
        assert response.status_code == 401

    @pytest.mark.regression
    @pytest.mark.parametrize("username,password,expected_status", [
        ("", "emilyspass", 400),
        ("emilys", "", 400),
        ("", "", 400),
    ])
    @allure.title("Login with missing credentials — parametrized")
    def test_login_missing_credentials(
        self, api: ApiFacade, username: str, password: str, expected_status: int
    ):
        flow = login_invalid_flow(username=username, password=password, api=api)
        assert flow["login"]["status_code"] == expected_status

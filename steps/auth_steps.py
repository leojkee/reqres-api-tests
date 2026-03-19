import allure

from api.api_facade import ApiFacade
from model.auth_model import LoginResponse, RefreshResponse, MeResponse
from wrappers import step


@step("Login and verify profile")
def login_flow(username: str, password: str, api: ApiFacade) -> dict:
    results = {}

    with allure.step("STEP 1: Login"):
        response = api.auth.login(username, password)
        response.raise_for_status()
        data = LoginResponse(**response.json())
        api.set_auth_token("Bearer", data.accessToken)
        results["login"] = response.json()

    with allure.step("STEP 2: Get current user profile"):
        response = api.auth.get_me()
        response.raise_for_status()
        MeResponse(**response.json())
        results["me"] = response.json()

    return results


@step("Login and refresh token")
def login_and_refresh_flow(username: str, password: str, api: ApiFacade) -> dict:
    results = {}

    with allure.step("STEP 1: Login"):
        response = api.auth.login(username, password)
        response.raise_for_status()
        data = LoginResponse(**response.json())
        api.set_auth_token("Bearer", data.accessToken)
        results["login"] = response.json()

    with allure.step("STEP 2: Refresh token"):
        response = api.auth.refresh(data.refreshToken)
        response.raise_for_status()
        RefreshResponse(**response.json())
        results["refresh"] = response.json()
        api.set_auth_token("Bearer", results["refresh"]["accessToken"])

    return results


@step("Login with invalid credentials")
def login_invalid_flow(username: str, password: str, api: ApiFacade) -> dict:
    results = {}

    with allure.step(f"STEP 1: Login with username={repr(username)}"):
        response = api.auth.login(username, password)
        results["login"] = {
            "status_code": response.status_code,
            "body": response.json(),
        }

    return results

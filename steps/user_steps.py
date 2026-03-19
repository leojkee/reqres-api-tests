import allure

from api.api_facade import ApiFacade
from model.user_model import UserListResponse, UserData, CreateUserResponse
from wrappers import step


@step("Get paginated users")
def get_users_flow(api: ApiFacade, limit: int = 10, skip: int = 0) -> dict:
    results = {}

    with allure.step(f"STEP 1: GET /users limit={limit} skip={skip}"):
        response = api.users.get_users(limit=limit, skip=skip)
        response.raise_for_status()
        UserListResponse(**response.json())
        results["users"] = response.json()

    return results


@step("Get single user")
def get_user_flow(api: ApiFacade, user_id: int) -> dict:
    results = {}

    with allure.step(f"STEP 1: GET /users/{user_id}"):
        response = api.users.get_user(user_id)
        results["status_code"] = response.status_code
        if response.status_code == 200:
            UserData(**response.json())
            results["user"] = response.json()
        else:
            results["body"] = response.json()

    return results


@step("Search users")
def search_users_flow(api: ApiFacade, query: str) -> dict:
    results = {}

    with allure.step(f"STEP 1: GET /users/search?q={query}"):
        response = api.users.search_users(query)
        response.raise_for_status()
        UserListResponse(**response.json())
        results["search"] = response.json()

    return results


@step("Create user")
def create_user_flow(api: ApiFacade, first_name: str, last_name: str, age: int) -> dict:
    results = {}

    with allure.step("STEP 1: POST /users/add"):
        response = api.users.create_user(first_name, last_name, age)
        response.raise_for_status()
        CreateUserResponse(**response.json())
        results["created"] = response.json()

    return results


@step("Update user")
def update_user_flow(api: ApiFacade, user_id: int, **fields) -> dict:
    results = {}

    with allure.step(f"STEP 1: PUT /users/{user_id}"):
        response = api.users.update_user(user_id, **fields)
        response.raise_for_status()
        results["updated"] = response.json()

    return results


@step("Delete user")
def delete_user_flow(api: ApiFacade, user_id: int) -> dict:
    results = {}

    with allure.step(f"STEP 1: DELETE /users/{user_id}"):
        response = api.users.delete_user(user_id)
        response.raise_for_status()
        results["deleted"] = response.json()
        results["is_deleted"] = response.json().get("isDeleted", False)

    return results

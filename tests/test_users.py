import allure
import pytest

from api.api_facade import ApiFacade
from data.generators import random_string
from steps.user_steps import (
    get_users_flow,
    get_user_flow,
    search_users_flow,
    create_user_flow,
    update_user_flow,
    delete_user_flow,
)


@allure.feature("Users")
@allure.story("CRUD")
@allure.severity(allure.severity_level.NORMAL)
class TestUsers:

    @pytest.mark.smoke
    @pytest.mark.regression
    @allure.title("Get users list")
    @allure.description("""
    Verifies users list endpoint returns paginated data.

    Expected result:
    - users list is non-empty.
    - total > 0.
    """)
    def test_get_users(self, api: ApiFacade):
        flow = get_users_flow(api=api, limit=5, skip=0)
        assert len(flow["users"]["users"]) == 5
        assert flow["users"]["total"] > 0

    @pytest.mark.regression
    @pytest.mark.parametrize("limit,skip", [(5, 0), (5, 5), (10, 0)])
    @allure.title("Get users — pagination")
    def test_get_users_pagination(self, api: ApiFacade, limit: int, skip: int):
        flow = get_users_flow(api=api, limit=limit, skip=skip)
        assert flow["users"]["limit"] == limit
        assert flow["users"]["skip"] == skip

    @pytest.mark.smoke
    @pytest.mark.regression
    @allure.title("Get single user by ID")
    def test_get_single_user(self, api: ApiFacade):
        flow = get_user_flow(api=api, user_id=1)
        assert flow["status_code"] == 200
        assert flow["user"]["id"] == 1

    @pytest.mark.regression
    @allure.title("Get non-existent user — 404")
    def test_get_user_not_found(self, api: ApiFacade):
        flow = get_user_flow(api=api, user_id=9999)
        assert flow["status_code"] == 404

    @pytest.mark.regression
    @allure.title("Search users by name")
    def test_search_users(self, api: ApiFacade):
        flow = search_users_flow(api=api, query="John")
        assert isinstance(flow["search"]["users"], list)

    @pytest.mark.smoke
    @pytest.mark.regression
    @allure.title("Create new user")
    @allure.description("""
    Verifies user creation.

    Expected result:
    - New user has an id.
    - firstName, lastName, age match request.
    """)
    def test_create_user(self, api: ApiFacade):
        first_name = random_string().capitalize()
        last_name = random_string().capitalize()
        flow = create_user_flow(api=api, first_name=first_name, last_name=last_name, age=25)
        assert flow["created"]["id"]
        assert flow["created"]["firstName"] == first_name
        assert flow["created"]["lastName"] == last_name

    @pytest.mark.regression
    @allure.title("Update user — change lastName")
    def test_update_user(self, api: ApiFacade):
        new_last_name = random_string().capitalize()
        flow = update_user_flow(api=api, user_id=1, lastName=new_last_name)
        assert flow["updated"]["lastName"] == new_last_name

    @pytest.mark.regression
    @allure.title("Delete user — isDeleted=True")
    def test_delete_user(self, api: ApiFacade):
        flow = delete_user_flow(api=api, user_id=1)
        assert flow["is_deleted"] is True

from functools import lru_cache

from infrastructure.db.database import get_database
from infrastructure.db.models import TestUser
from infrastructure.db.repositories import TestUserRepository


@lru_cache(maxsize=1)
def get_active_users() -> list[TestUser]:
    db = get_database()
    with db.session() as session:
        repo = TestUserRepository(session)
        return repo.get_active_users()


@lru_cache(maxsize=1)
def get_super_user() -> list[TestUser]:
    db = get_database()
    with db.session() as session:
        repo = TestUserRepository(session)
        users = repo.get_by_tags("super_user")
        if not users:
            raise RuntimeError("No super_user found in DB. Run seed_data.py first.")
        return users


def clear_cache():
    get_active_users.cache_clear()
    get_super_user.cache_clear()

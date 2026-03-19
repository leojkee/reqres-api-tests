import pytest
from sqlalchemy.orm import Session

from infrastructure.db.database import Database, get_database
from infrastructure.db.repositories import TestUserRepository


@pytest.fixture(scope="session")
def database() -> Database:
    return get_database()


@pytest.fixture(scope="function")
def db_session(database: Database) -> Session:
    with database.session() as session:
        yield session


@pytest.fixture(scope="function")
def test_user_repository(db_session: Session) -> TestUserRepository:
    return TestUserRepository(db_session)

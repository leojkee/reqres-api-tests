from sqlalchemy import select
from sqlalchemy.orm import Session

from infrastructure.db.models.test_user import TestUser, TestUserRole
from infrastructure.db.repositories.base_repository import BaseRepository
from utils.encryption import encrypt_password, decrypt_password


class TestUserRepository(BaseRepository[TestUser]):

    def __init__(self, session: Session):
        super().__init__(session, TestUser)

    def get_by_username(self, username: str) -> TestUser | None:
        stmt = select(TestUser).where(TestUser.username == username)
        return self.session.execute(stmt).scalar_one_or_none()

    def get_by_email(self, email: str) -> TestUser | None:
        stmt = select(TestUser).where(TestUser.email == email)
        return self.session.execute(stmt).scalar_one_or_none()

    def get_by_role(self, role: str) -> list[TestUser]:
        stmt = (
            select(TestUser)
            .where(TestUser.role == TestUserRole[role.upper()])
            .where(TestUser.is_active)
        )
        return list(self.session.execute(stmt).scalars().all())

    def get_active_users(self) -> list[TestUser]:
        stmt = select(TestUser).where(TestUser.is_active)
        return list(self.session.execute(stmt).scalars().all())

    def get_by_tags(self, tags: str | list[str]) -> list[TestUser]:
        tag_list = [tags] if isinstance(tags, str) else tags
        stmt = (
            select(TestUser)
            .where(TestUser.is_active)
            .where(TestUser.tags.contains(tag_list))
        )
        return list(self.session.execute(stmt).scalars().all())

    def get_decrypted_password(self, user: TestUser) -> str:
        return decrypt_password(user.password_encrypted)

    def get_decrypted_mfa_hash(self, user: TestUser) -> str | None:
        if user.google_mfa_hash_encrypted:
            return decrypt_password(user.google_mfa_hash_encrypted)
        return None

    def create_with_encrypted_password(
        self,
        username: str,
        email: str,
        password: str,
        google_mfa_hash: str | None = None,
        role: TestUserRole = TestUserRole.B2C,
        account_id: int | None = None,
        is_active: bool = True,
        tags: list[str] | None = None,
    ) -> TestUser:
        user = TestUser(
            username=username,
            email=email,
            password_encrypted=encrypt_password(password),
            google_mfa_hash_encrypted=encrypt_password(google_mfa_hash) if google_mfa_hash else None,
            role=role,
            account_id=account_id,
            is_active=is_active,
            tags=tags,
        )
        return self.create(user)

import enum

from sqlalchemy import Boolean, Enum, Integer, LargeBinary, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.db.base import Base


class TestUserRole(enum.Enum):
    B2C = "B2C"
    ADMIN = "ADMIN"


class TestUser(Base):
    __tablename__ = "test_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password_encrypted: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    google_mfa_hash_encrypted: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
    role: Mapped[TestUserRole] = mapped_column(Enum(TestUserRole), default=TestUserRole.B2C)
    account_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    tags: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)


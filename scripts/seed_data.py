import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from infrastructure.db.database import get_database
from infrastructure.db.models.test_user import TestUserRole
from infrastructure.db.repositories.test_user_repository import TestUserRepository

USERS = [
    {
        "username": "emilys",
        "email": "emily.johnson@x.dummyjson.com",
        "password": "emilyspass",
        "google_mfa_hash": None,
        "role": TestUserRole.B2C,
        "account_id": 1,
        "tags": ["super_user", "b2c"],
    },
    {
        "username": "michaelw",
        "email": "michael.williams@x.dummyjson.com",
        "password": "michaelwpass",
        "google_mfa_hash": None,
        "role": TestUserRole.ADMIN,
        "account_id": 2,
        "tags": ["admin"],
    },
]


def seed(clear: bool = False):
    db = get_database()
    with db.session() as session:
        repo = TestUserRepository(session)

        if clear:
            for user in repo.get_all():
                repo.delete(user)
            print("cleared existing users")

        for data in USERS:
            if repo.get_by_username(data["username"]):
                print(f"skip: {data['username']} already exists")
                continue

            repo.create_with_encrypted_password(
                username=data["username"],
                email=data["email"],
                password=data["password"],
                google_mfa_hash=data["google_mfa_hash"],
                role=data["role"],
                account_id=data["account_id"],
                tags=data["tags"],
            )
            print(f"created: {data['username']} ({data['role'].value})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--clear", action="store_true")
    args = parser.parse_args()
    seed(clear=args.clear)

from cryptography.fernet import Fernet

from utils.config import settings


def _get_fernet() -> Fernet:
    return Fernet(settings.ENCRYPTION_KEY.encode())


def encrypt_password(plain: str) -> bytes:
    return _get_fernet().encrypt(plain.encode())


def decrypt_password(encrypted: bytes) -> str:
    return _get_fernet().decrypt(encrypted).decode()

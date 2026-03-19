import pytest

from mfa.googleauth.google_auth_service import GoogleAuthService
from mfa.googleauth.google_client import GoogleAuthClient
from mfa.mfa_client import MFAClient


@pytest.fixture(scope="session")
def google_auth_client() -> MFAClient:
    return GoogleAuthClient(GoogleAuthService())

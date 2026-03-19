from mfa.googleauth.google_auth_service import GoogleAuthService
from mfa.mfa_client import MFAClient


class GoogleAuthClient(MFAClient):

    def __init__(self, service: GoogleAuthService):
        self._service = service

    def get_otp(self, secret: str) -> str:
        return self._service.get_otp(secret)

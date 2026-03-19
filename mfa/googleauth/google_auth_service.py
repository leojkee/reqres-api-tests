import pyotp


class GoogleAuthService:

    def get_otp(self, secret: str) -> str:
        totp = pyotp.TOTP(secret)
        return totp.now()

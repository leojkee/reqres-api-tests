_SENSITIVE_FIELDS = {
    "password", "token", "access_token", "refresh_token",
    "secret", "authorization", "encrypted", "mfa", "otp",
}


def get_sensitive_test_params() -> set[str]:
    return _SENSITIVE_FIELDS


def mask_value(value: str, visible_chars: int = 4) -> str:
    if len(value) <= visible_chars:
        return "***"
    return value[:visible_chars] + "***"


def mask_sensitive(text: str) -> str:
    """Mask known sensitive substrings in arbitrary text."""
    for keyword in _SENSITIVE_FIELDS:
        if keyword in text.lower():
            return "[MASKED]"
    return text

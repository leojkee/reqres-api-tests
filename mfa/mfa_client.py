from abc import ABC, abstractmethod


class MFAClient(ABC):

    @abstractmethod
    def get_otp(self, secret: str) -> str: ...

from pydantic import BaseModel


class LoginResponse(BaseModel):
    accessToken: str
    refreshToken: str
    id: int
    username: str
    email: str
    firstName: str
    lastName: str


class RefreshResponse(BaseModel):
    accessToken: str
    refreshToken: str


class MeResponse(BaseModel):
    id: int
    username: str
    email: str
    firstName: str
    lastName: str

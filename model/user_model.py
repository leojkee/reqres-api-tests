from pydantic import BaseModel


class UserData(BaseModel):
    id: int
    firstName: str
    lastName: str
    email: str
    username: str
    age: int


class UserListResponse(BaseModel):
    users: list[UserData]
    total: int
    skip: int
    limit: int


class CreateUserResponse(BaseModel):
    id: int
    firstName: str
    lastName: str
    age: int

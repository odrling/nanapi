from uuid import UUID

from pydantic import BaseModel


class NewClientBody(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str


class WhoamiResponse(BaseModel):
    id: UUID
    username: str

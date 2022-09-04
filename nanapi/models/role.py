from pydantic import BaseModel


class NewRoleBody(BaseModel):
    role_id: int
    emoji: str

from pydantic import BaseModel


class CollectPotBody(BaseModel):
    discord_username: str
    amount: float

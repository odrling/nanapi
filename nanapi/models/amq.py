from typing import Any

from pydantic import BaseModel, Json


class UpsertAMQAccountBody(BaseModel):
    discord_username: str
    username: str


class UpdateAMQSettingsBody(BaseModel):
    settings: Json[Any]

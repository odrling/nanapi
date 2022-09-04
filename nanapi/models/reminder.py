from datetime import datetime

from pydantic import BaseModel


class NewReminderBody(BaseModel):
    discord_id: int
    discord_username: str
    channel_id: int
    message: str
    timestamp: datetime

from datetime import datetime
from uuid import UUID

from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
select reminder::Reminder {
  id,
  channel_id,
  channel_id_str,
  message,
  timestamp,
  user: {
    discord_id,
    discord_id_str,
  },
}
filter .client = global client
"""


class ReminderSelectAllResultUser(BaseModel):
    discord_id: int
    discord_id_str: str


class ReminderSelectAllResult(BaseModel):
    id: UUID
    channel_id: int
    channel_id_str: str
    message: str
    timestamp: datetime
    user: ReminderSelectAllResultUser


adapter = TypeAdapter(list[ReminderSelectAllResult])


async def reminder_select_all(
    executor: AsyncIOExecutor,
) -> list[ReminderSelectAllResult]:
    resp = await executor.query_json(
        EDGEQL_QUERY,
    )
    return adapter.validate_json(resp, strict=False)

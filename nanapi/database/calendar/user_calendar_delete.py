from uuid import UUID

from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  discord_id := <int64>$discord_id
delete calendar::UserCalendar
filter .user.discord_id = discord_id
"""


class UserCalendarDeleteResult(BaseModel):
    id: UUID


adapter = TypeAdapter(UserCalendarDeleteResult | None)


async def user_calendar_delete(
    executor: AsyncIOExecutor,
    *,
    discord_id: int,
) -> UserCalendarDeleteResult | None:
    resp = await executor.query_single_json(
        EDGEQL_QUERY,
        discord_id=discord_id,
    )
    return adapter.validate_json(resp, strict=False)

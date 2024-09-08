from uuid import UUID

from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  discord_id := <int64>$discord_id
select assert_single(calendar::UserCalendar) {
  ics,
  user: { * },
}
filter .user.discord_id = discord_id
"""


class UserCalendarSelectResultUser(BaseModel):
    id: UUID
    discord_id: int
    discord_id_str: str
    discord_username: str


class UserCalendarSelectResult(BaseModel):
    ics: str
    user: UserCalendarSelectResultUser


adapter = TypeAdapter(UserCalendarSelectResult | None)


async def user_calendar_select(
    executor: AsyncIOExecutor,
    *,
    discord_id: int,
) -> UserCalendarSelectResult | None:
    resp = await executor.query_single_json(
        EDGEQL_QUERY,
        discord_id=discord_id,
    )
    return adapter.validate_json(resp, strict=False)

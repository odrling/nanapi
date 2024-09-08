from uuid import UUID

from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
select calendar::UserCalendar {
  ics,
  user: { * },
}
"""


class UserCalendarSelectAllResultUser(BaseModel):
    id: UUID
    discord_id: int
    discord_id_str: str
    discord_username: str


class UserCalendarSelectAllResult(BaseModel):
    ics: str
    user: UserCalendarSelectAllResultUser


adapter = TypeAdapter(list[UserCalendarSelectAllResult])


async def user_calendar_select_all(
    executor: AsyncIOExecutor,
) -> list[UserCalendarSelectAllResult]:
    resp = await executor.query_json(
        EDGEQL_QUERY,
    )
    return adapter.validate_json(resp, strict=False)

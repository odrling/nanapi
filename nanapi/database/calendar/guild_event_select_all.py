from datetime import datetime
from uuid import UUID

from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  start_after := <optional datetime>$start_after,
select calendar::GuildEvent {
  *,
  organizer: { * },
  participants: { * },
}
filter .client = global client
and (.start_time > start_after if exists start_after else true)
"""


class GuildEventSelectAllResultParticipants(BaseModel):
    id: UUID
    discord_id: int
    discord_id_str: str
    discord_username: str


class GuildEventSelectAllResultOrganizer(BaseModel):
    id: UUID
    discord_id: int
    discord_id_str: str
    discord_username: str


class GuildEventSelectAllResult(BaseModel):
    organizer: GuildEventSelectAllResultOrganizer
    participants: list[GuildEventSelectAllResultParticipants]
    id: UUID
    discord_id: int
    description: str | None
    discord_id_str: str
    end_time: datetime
    image: str | None
    location: str | None
    name: str
    start_time: datetime
    url: str | None


adapter = TypeAdapter(list[GuildEventSelectAllResult])


async def guild_event_select_all(
    executor: AsyncIOExecutor,
    *,
    start_after: datetime | None = None,
) -> list[GuildEventSelectAllResult]:
    resp = await executor.query_json(
        EDGEQL_QUERY,
        start_after=start_after,
    )
    return adapter.validate_json(resp, strict=False)

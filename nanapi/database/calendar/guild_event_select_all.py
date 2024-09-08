from datetime import datetime
from uuid import UUID

from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
select calendar::GuildEvent {
  *,
  organizer: { * },
  participants: { * },
}
filter .client = global client
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
) -> list[GuildEventSelectAllResult]:
    resp = await executor.query_json(
        EDGEQL_QUERY,
    )
    return adapter.validate_json(resp, strict=False)

from datetime import datetime
from uuid import UUID

from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  discord_id := <int64>$discord_id,
select calendar::GuildEvent {
  *,
  organizer: { * },
  participants: { * },
}
filter .client = global client
and .participants.discord_id = discord_id
"""


class GuildEventSelectParticipantResultParticipants(BaseModel):
    id: UUID
    discord_id: int
    discord_id_str: str
    discord_username: str


class GuildEventSelectParticipantResultOrganizer(BaseModel):
    id: UUID
    discord_id: int
    discord_id_str: str
    discord_username: str


class GuildEventSelectParticipantResult(BaseModel):
    organizer: GuildEventSelectParticipantResultOrganizer
    participants: list[GuildEventSelectParticipantResultParticipants]
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


adapter = TypeAdapter(list[GuildEventSelectParticipantResult])


async def guild_event_select_participant(
    executor: AsyncIOExecutor,
    *,
    discord_id: int,
) -> list[GuildEventSelectParticipantResult]:
    resp = await executor.query_json(
        EDGEQL_QUERY,
        discord_id=discord_id,
    )
    return adapter.validate_json(resp, strict=False)

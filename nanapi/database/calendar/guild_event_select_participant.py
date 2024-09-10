from datetime import datetime
from enum import StrEnum
from uuid import UUID

from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  discord_id := <int64>$discord_id,
select calendar::GuildEvent { ** }
filter .client = global client
and .participants.discord_id = discord_id
"""


class ProjectionStatus(StrEnum):
    ONGOING = 'ONGOING'
    COMPLETED = 'COMPLETED'


class GuildEventSelectParticipantResultProjection(BaseModel):
    id: UUID
    channel_id: int
    channel_id_str: str
    message_id: int | None
    message_id_str: str | None
    name: str
    status: ProjectionStatus


class GuildEventSelectParticipantResultOrganizer(BaseModel):
    id: UUID
    discord_id: int
    discord_id_str: str
    discord_username: str


class GuildEventSelectParticipantResultParticipants(BaseModel):
    id: UUID
    discord_id: int
    discord_id_str: str
    discord_username: str


class GuildEventSelectParticipantResultClient(BaseModel):
    id: UUID
    password_hash: str
    username: str


class GuildEventSelectParticipantResult(BaseModel):
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
    client: GuildEventSelectParticipantResultClient
    participants: list[GuildEventSelectParticipantResultParticipants]
    organizer: GuildEventSelectParticipantResultOrganizer
    projection: GuildEventSelectParticipantResultProjection | None


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

from datetime import datetime
from enum import StrEnum
from uuid import UUID

from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  start_after := <optional datetime>$start_after,
select calendar::GuildEvent { ** }
filter .client = global client
and (.start_time > start_after if exists start_after else true)
"""


class ProjectionStatus(StrEnum):
    ONGOING = 'ONGOING'
    COMPLETED = 'COMPLETED'


class GuildEventSelectAllResultProjection(BaseModel):
    id: UUID
    channel_id: int
    channel_id_str: str
    message_id: int | None
    message_id_str: str | None
    name: str
    status: ProjectionStatus


class GuildEventSelectAllResultOrganizer(BaseModel):
    id: UUID
    discord_id: int
    discord_id_str: str
    discord_username: str


class GuildEventSelectAllResultParticipants(BaseModel):
    id: UUID
    discord_id: int
    discord_id_str: str
    discord_username: str


class GuildEventSelectAllResultClient(BaseModel):
    id: UUID
    password_hash: str
    username: str


class GuildEventSelectAllResult(BaseModel):
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
    client: GuildEventSelectAllResultClient
    participants: list[GuildEventSelectAllResultParticipants]
    organizer: GuildEventSelectAllResultOrganizer
    projection: GuildEventSelectAllResultProjection | None


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

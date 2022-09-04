from enum import StrEnum
from uuid import UUID

from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
select presence::Presence { id, type, name }
filter .client = global client
"""


class PresencePresenceType(StrEnum):
    PLAYING = 'PLAYING'
    LISTENING = 'LISTENING'
    WATCHING = 'WATCHING'


class PresenceSelectAllResult(BaseModel):
    id: UUID
    type: PresencePresenceType
    name: str


adapter = TypeAdapter(list[PresenceSelectAllResult])


async def presence_select_all(
    executor: AsyncIOExecutor,
) -> list[PresenceSelectAllResult]:
    resp = await executor.query_json(
        EDGEQL_QUERY,
    )
    return adapter.validate_json(resp, strict=False)

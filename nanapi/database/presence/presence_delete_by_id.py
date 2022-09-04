from uuid import UUID

from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
delete presence::Presence filter .id = <uuid>$id
"""


class PresenceDeleteByIdResult(BaseModel):
    id: UUID


adapter = TypeAdapter(PresenceDeleteByIdResult | None)


async def presence_delete_by_id(
    executor: AsyncIOExecutor,
    *,
    id: UUID,
) -> PresenceDeleteByIdResult | None:
    resp = await executor.query_single_json(
        EDGEQL_QUERY,
        id=id,
    )
    return adapter.validate_json(resp, strict=False)

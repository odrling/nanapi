from uuid import UUID

from gel import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  id := <uuid>$id,
update projection::Projection
filter .id = id
set {
  guild_events -= (select .guild_events filter .start_time > datetime_of_transaction())
}
"""


class ProjoDeleteUpcomingEventsResult(BaseModel):
    id: UUID


adapter = TypeAdapter(ProjoDeleteUpcomingEventsResult | None)


async def projo_delete_upcoming_events(
    executor: AsyncIOExecutor,
    *,
    id: UUID,
) -> ProjoDeleteUpcomingEventsResult | None:
    resp = await executor.query_single_json(
        EDGEQL_QUERY,
        id=id,
    )
    return adapter.validate_json(resp, strict=False)

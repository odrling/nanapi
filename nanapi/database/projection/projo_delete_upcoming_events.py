from uuid import UUID

from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  id := <uuid>$id,
  projo := (select projection::Projection filter .id = id)
delete projection::Event
filter .projection = projo and .date > datetime_current()
"""


class ProjoDeleteUpcomingEventsResult(BaseModel):
    id: UUID


adapter = TypeAdapter(list[ProjoDeleteUpcomingEventsResult])


async def projo_delete_upcoming_events(
    executor: AsyncIOExecutor,
    *,
    id: UUID,
) -> list[ProjoDeleteUpcomingEventsResult]:
    resp = await executor.query_json(
        EDGEQL_QUERY,
        id=id,
    )
    return adapter.validate_json(resp, strict=False)

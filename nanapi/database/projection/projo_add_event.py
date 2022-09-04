from datetime import datetime
from uuid import UUID

from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  id := <uuid>$id,
  date := <datetime>$date,
  description := <str>$description,
  projo := (select projection::Projection filter .id = id)
insert projection::Event {
  client := global client,
  date := date,
  description := description,
  projection := projo
}
"""


class ProjoAddEventResult(BaseModel):
    id: UUID


adapter = TypeAdapter(ProjoAddEventResult)


async def projo_add_event(
    executor: AsyncIOExecutor,
    *,
    id: UUID,
    date: datetime,
    description: str,
) -> ProjoAddEventResult:
    resp = await executor.query_single_json(
        EDGEQL_QUERY,
        id=id,
        date=date,
        description=description,
    )
    return adapter.validate_json(resp, strict=False)

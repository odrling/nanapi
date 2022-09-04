from uuid import UUID

from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  id := <uuid>$id,
  name := <str>$name,
update projection::Projection
filter .id = id
set { name := name }
"""


class ProjoUpdateNameResult(BaseModel):
    id: UUID


adapter = TypeAdapter(ProjoUpdateNameResult | None)


async def projo_update_name(
    executor: AsyncIOExecutor,
    *,
    id: UUID,
    name: str,
) -> ProjoUpdateNameResult | None:
    resp = await executor.query_single_json(
        EDGEQL_QUERY,
        id=id,
        name=name,
    )
    return adapter.validate_json(resp, strict=False)

from uuid import UUID

from gel import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  id := <uuid>$id,
delete projection::Projection
filter .id = id
"""


class ProjoDeleteResult(BaseModel):
    id: UUID


adapter = TypeAdapter(ProjoDeleteResult | None)


async def projo_delete(
    executor: AsyncIOExecutor,
    *,
    id: UUID,
) -> ProjoDeleteResult | None:
    resp = await executor.query_single_json(
        EDGEQL_QUERY,
        id=id,
    )
    return adapter.validate_json(resp, strict=False)

from uuid import UUID

from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
select histoire::Histoire {
  id,
  title,
  text,
  formatted,
}
filter .id = <uuid>$id
"""


class HistoireGetByIdResult(BaseModel):
    id: UUID
    title: str
    text: str
    formatted: bool


adapter = TypeAdapter(HistoireGetByIdResult | None)


async def histoire_get_by_id(
    executor: AsyncIOExecutor,
    *,
    id: UUID,
) -> HistoireGetByIdResult | None:
    resp = await executor.query_single_json(
        EDGEQL_QUERY,
        id=id,
    )
    return adapter.validate_json(resp, strict=False)

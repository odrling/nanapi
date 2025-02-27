from uuid import UUID

from gel import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  id := <uuid>$id,
delete waicolle::TradeOperation
filter .id = id
"""


class TradeDeleteResult(BaseModel):
    id: UUID


adapter = TypeAdapter(TradeDeleteResult | None)


async def trade_delete(
    executor: AsyncIOExecutor,
    *,
    id: UUID,
) -> TradeDeleteResult | None:
    resp = await executor.query_single_json(
        EDGEQL_QUERY,
        id=id,
    )
    return adapter.validate_json(resp, strict=False)

from uuid import UUID

from gel import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
delete histoire::Histoire filter .id = <uuid>$id
"""


class HistoireDeleteByIdResult(BaseModel):
    id: UUID


adapter = TypeAdapter(HistoireDeleteByIdResult | None)


async def histoire_delete_by_id(
    executor: AsyncIOExecutor,
    *,
    id: UUID,
) -> HistoireDeleteByIdResult | None:
    resp = await executor.query_single_json(
        EDGEQL_QUERY,
        id=id,
    )
    return adapter.validate_json(resp, strict=False)

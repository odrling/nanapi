from uuid import UUID

from gel import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  key := <str>$key,
delete redis::Data
filter .key = key
"""


class DataDeleteByKeyResult(BaseModel):
    id: UUID


adapter = TypeAdapter(DataDeleteByKeyResult | None)


async def data_delete_by_key(
    executor: AsyncIOExecutor,
    *,
    key: str,
) -> DataDeleteByKeyResult | None:
    resp = await executor.query_single_json(
        EDGEQL_QUERY,
        key=key,
    )
    return adapter.validate_json(resp, strict=False)

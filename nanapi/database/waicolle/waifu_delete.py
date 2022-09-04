from uuid import UUID

from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  ids := <array<uuid>>$ids,
delete waicolle::Waifu
filter .id in array_unpack(ids)
"""


class WaifuDeleteResult(BaseModel):
    id: UUID


adapter = TypeAdapter(list[WaifuDeleteResult])


async def waifu_delete(
    executor: AsyncIOExecutor,
    *,
    ids: list[UUID],
) -> list[WaifuDeleteResult]:
    resp = await executor.query_json(
        EDGEQL_QUERY,
        ids=ids,
    )
    return adapter.validate_json(resp, strict=False)

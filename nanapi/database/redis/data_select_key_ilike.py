from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  pattern := <str>$pattern,
select redis::Data {
  key,
}
filter .key ilike pattern
"""


class DataSelectKeyIlikeResult(BaseModel):
    key: str


adapter = TypeAdapter(list[DataSelectKeyIlikeResult])


async def data_select_key_ilike(
    executor: AsyncIOExecutor,
    *,
    pattern: str,
) -> list[DataSelectKeyIlikeResult]:
    resp = await executor.query_json(
        EDGEQL_QUERY,
        pattern=pattern,
    )
    return adapter.validate_json(resp, strict=False)

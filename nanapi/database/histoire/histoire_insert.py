from uuid import UUID

from gel import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  title := <str>$title,
  text := <str>$text,
insert histoire::Histoire{
  client := global client,
  title := title,
  text := text,
}
"""


class HistoireInsertResult(BaseModel):
    id: UUID


adapter = TypeAdapter(HistoireInsertResult)


async def histoire_insert(
    executor: AsyncIOExecutor,
    *,
    title: str,
    text: str,
) -> HistoireInsertResult:
    resp = await executor.query_single_json(
        EDGEQL_QUERY,
        title=title,
        text=text,
    )
    return adapter.validate_json(resp, strict=False)

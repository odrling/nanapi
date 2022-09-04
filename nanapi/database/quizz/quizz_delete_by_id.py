from uuid import UUID

from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  id := <uuid>$id
delete quizz::Quizz
filter .id = id
"""


class QuizzDeleteByIdResult(BaseModel):
    id: UUID


adapter = TypeAdapter(QuizzDeleteByIdResult | None)


async def quizz_delete_by_id(
    executor: AsyncIOExecutor,
    *,
    id: UUID,
) -> QuizzDeleteByIdResult | None:
    resp = await executor.query_single_json(
        EDGEQL_QUERY,
        id=id,
    )
    return adapter.validate_json(resp, strict=False)

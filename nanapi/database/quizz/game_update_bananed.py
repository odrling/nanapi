from uuid import UUID

from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  id := <uuid>$id,
  answer_bananed := <optional str>$answer_bananed,
update quizz::Game
filter .id = id
set {
  answer_bananed := answer_bananed,
}
"""


class GameUpdateBananedResult(BaseModel):
    id: UUID


adapter = TypeAdapter(GameUpdateBananedResult | None)


async def game_update_bananed(
    executor: AsyncIOExecutor,
    *,
    id: UUID,
    answer_bananed: str | None = None,
) -> GameUpdateBananedResult | None:
    resp = await executor.query_single_json(
        EDGEQL_QUERY,
        id=id,
        answer_bananed=answer_bananed,
    )
    return adapter.validate_json(resp, strict=False)

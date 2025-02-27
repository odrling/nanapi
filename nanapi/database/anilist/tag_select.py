from gel import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
select anilist::Tag {
  id_al,
  name,
  description,
  category,
  is_adult,
}
"""


class TagSelectResult(BaseModel):
    id_al: int
    name: str
    description: str
    category: str
    is_adult: bool


adapter = TypeAdapter(list[TagSelectResult])


async def tag_select(
    executor: AsyncIOExecutor,
) -> list[TagSelectResult]:
    resp = await executor.query_json(
        EDGEQL_QUERY,
    )
    return adapter.validate_json(resp, strict=False)

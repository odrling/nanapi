from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
select anilist::Media {
  id_al,
}
filter .is_adult
order by .favourites desc
limit 1000
"""


class MediaSelectTopHResult(BaseModel):
    id_al: int


adapter = TypeAdapter(list[MediaSelectTopHResult])


async def media_select_top_h(
    executor: AsyncIOExecutor,
) -> list[MediaSelectTopHResult]:
    resp = await executor.query_json(
        EDGEQL_QUERY,
    )
    return adapter.validate_json(resp, strict=False)

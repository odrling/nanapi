from enum import StrEnum

from gel import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
select anilist::Media {
  type,
  id_al,
  id_mal
}
"""


class AnilistMediaType(StrEnum):
    ANIME = 'ANIME'
    MANGA = 'MANGA'


class MediaSelectAllIdsResult(BaseModel):
    type: AnilistMediaType
    id_al: int
    id_mal: int | None


adapter = TypeAdapter(list[MediaSelectAllIdsResult])


async def media_select_all_ids(
    executor: AsyncIOExecutor,
) -> list[MediaSelectAllIdsResult]:
    resp = await executor.query_json(
        EDGEQL_QUERY,
    )
    return adapter.validate_json(resp, strict=False)

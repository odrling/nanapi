from enum import StrEnum

from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
select anilist::Media {
  id_al,
  type,
  title_user_preferred,
  title_native,
  title_english,
  synonyms,
}
order by .favourites desc
"""


class AnilistMediaType(StrEnum):
    ANIME = 'ANIME'
    MANGA = 'MANGA'


class MediaSelectAllTitlesResult(BaseModel):
    id_al: int
    type: AnilistMediaType
    title_user_preferred: str
    title_native: str | None
    title_english: str | None
    synonyms: list[str]


adapter = TypeAdapter(list[MediaSelectAllTitlesResult])


async def media_select_all_titles(
    executor: AsyncIOExecutor,
) -> list[MediaSelectAllTitlesResult]:
    resp = await executor.query_json(
        EDGEQL_QUERY,
    )
    return adapter.validate_json(resp, strict=False)

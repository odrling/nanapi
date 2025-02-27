from gel import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
select anilist::Media {
  id_al,
}
filter .type = anilist::MediaType.ANIME
and .status = anilist::MediaStatus.NOT_YET_RELEASED
"""


class AnimeSelectIdsUpcomingResult(BaseModel):
    id_al: int


adapter = TypeAdapter(list[AnimeSelectIdsUpcomingResult])


async def anime_select_ids_upcoming(
    executor: AsyncIOExecutor,
) -> list[AnimeSelectIdsUpcomingResult]:
    resp = await executor.query_json(
        EDGEQL_QUERY,
    )
    return adapter.validate_json(resp, strict=False)

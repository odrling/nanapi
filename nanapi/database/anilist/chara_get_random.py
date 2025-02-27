from enum import StrEnum

from gel import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
select anilist::Character {
  id_al,
  favourites,
  site_url,
  name_user_preferred,
  name_alternative,
  name_alternative_spoiler,
  name_native,
  description,
  image_large,
  gender,
  age,
  date_of_birth_year,
  date_of_birth_month,
  date_of_birth_day,
  rank,
  fuzzy_gender,
}
order by random()
limit 1
"""


class WaicolleRank(StrEnum):
    S = 'S'
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    E = 'E'


class CharaGetRandomResult(BaseModel):
    id_al: int
    favourites: int
    site_url: str
    name_user_preferred: str
    name_alternative: list[str]
    name_alternative_spoiler: list[str]
    name_native: str | None
    description: str | None
    image_large: str
    gender: str | None
    age: str | None
    date_of_birth_year: int | None
    date_of_birth_month: int | None
    date_of_birth_day: int | None
    rank: WaicolleRank
    fuzzy_gender: str | None


adapter = TypeAdapter(CharaGetRandomResult | None)


async def chara_get_random(
    executor: AsyncIOExecutor,
) -> CharaGetRandomResult | None:
    resp = await executor.query_single_json(
        EDGEQL_QUERY,
    )
    return adapter.validate_json(resp, strict=False)

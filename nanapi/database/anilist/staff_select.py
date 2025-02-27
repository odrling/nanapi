from gel import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  ids_al := <array<int32>>$ids_al
select anilist::Staff {
  id_al,
  favourites,
  site_url,
  name_user_preferred,
  name_native,
  name_alternative,
  description,
  image_large,
  gender,
  age,
  date_of_birth_year,
  date_of_birth_month,
  date_of_birth_day,
  date_of_death_year,
  date_of_death_month,
  date_of_death_day,
} filter .id_al in array_unpack(ids_al)
"""


class StaffSelectResult(BaseModel):
    id_al: int
    favourites: int
    site_url: str
    name_user_preferred: str
    name_native: str | None
    name_alternative: list[str]
    description: str | None
    image_large: str
    gender: str | None
    age: int | None
    date_of_birth_year: int | None
    date_of_birth_month: int | None
    date_of_birth_day: int | None
    date_of_death_year: int | None
    date_of_death_month: int | None
    date_of_death_day: int | None


adapter = TypeAdapter(list[StaffSelectResult])


async def staff_select(
    executor: AsyncIOExecutor,
    *,
    ids_al: list[int],
) -> list[StaffSelectResult]:
    resp = await executor.query_json(
        EDGEQL_QUERY,
        ids_al=ids_al,
    )
    return adapter.validate_json(resp, strict=False)

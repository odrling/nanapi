from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  pattern := <str>$pattern
select user::Profile {
  full_name,
  photo,
  promotion,
  telephone,
  user: {
    discord_id,
    discord_id_str,
  },
}
filter .full_name ilike pattern or .promotion ilike pattern or .telephone ilike pattern
"""


class ProfileSelectIlikeResultUser(BaseModel):
    discord_id: int
    discord_id_str: str


class ProfileSelectIlikeResult(BaseModel):
    full_name: str | None
    photo: str | None
    promotion: str | None
    telephone: str | None
    user: ProfileSelectIlikeResultUser


adapter = TypeAdapter(list[ProfileSelectIlikeResult])


async def profile_select_ilike(
    executor: AsyncIOExecutor,
    *,
    pattern: str,
) -> list[ProfileSelectIlikeResult]:
    resp = await executor.query_json(
        EDGEQL_QUERY,
        pattern=pattern,
    )
    return adapter.validate_json(resp, strict=False)

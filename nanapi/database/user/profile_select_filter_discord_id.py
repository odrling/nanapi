from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  discord_ids := <array<int64>>$discord_ids,
  _discord_ids := array_unpack(discord_ids),
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
filter .user.discord_id in _discord_ids
order by .full_name
"""


class ProfileSelectFilterDiscordIdResultUser(BaseModel):
    discord_id: int
    discord_id_str: str


class ProfileSelectFilterDiscordIdResult(BaseModel):
    full_name: str | None
    photo: str | None
    promotion: str | None
    telephone: str | None
    user: ProfileSelectFilterDiscordIdResultUser


adapter = TypeAdapter(list[ProfileSelectFilterDiscordIdResult])


async def profile_select_filter_discord_id(
    executor: AsyncIOExecutor,
    *,
    discord_ids: list[int],
) -> list[ProfileSelectFilterDiscordIdResult]:
    resp = await executor.query_json(
        EDGEQL_QUERY,
        discord_ids=discord_ids,
    )
    return adapter.validate_json(resp, strict=False)

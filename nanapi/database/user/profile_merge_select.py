from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  discord_id := <int64>$discord_id,
  discord_username := <str>$discord_username,
  full_name := <optional str>$full_name,
  photo := <optional str>$photo,
  promotion := <optional str>$promotion,
  telephone := <optional str>$telephone,
  user := (
    insert user::User {
      discord_id := discord_id,
      discord_username := discord_username,
    }
    unless conflict on .discord_id
    else (
      update user::User set {
        discord_username := discord_username,
      }
    )
  ),
  profile := (
    insert user::Profile {
      full_name := full_name,
      photo := photo,
      promotion := promotion,
      telephone := telephone,
      user := user,
    }
    unless conflict on .user
    else (
      update user::Profile set {
        full_name := full_name,
        photo := photo,
        promotion := promotion,
        telephone := telephone,
      }
    )
  )
select profile {
  full_name,
  photo,
  promotion,
  telephone,
  user: {
    discord_id,
    discord_id_str,
  },
}
"""


class ProfileMergeSelectResultUser(BaseModel):
    discord_id: int
    discord_id_str: str


class ProfileMergeSelectResult(BaseModel):
    full_name: str | None
    photo: str | None
    promotion: str | None
    telephone: str | None
    user: ProfileMergeSelectResultUser


adapter = TypeAdapter(ProfileMergeSelectResult)


async def profile_merge_select(
    executor: AsyncIOExecutor,
    *,
    discord_id: int,
    discord_username: str,
    full_name: str | None = None,
    photo: str | None = None,
    promotion: str | None = None,
    telephone: str | None = None,
) -> ProfileMergeSelectResult:
    resp = await executor.query_single_json(
        EDGEQL_QUERY,
        discord_id=discord_id,
        discord_username=discord_username,
        full_name=full_name,
        photo=photo,
        promotion=promotion,
        telephone=telephone,
    )
    return adapter.validate_json(resp, strict=False)

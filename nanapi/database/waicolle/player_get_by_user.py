from enum import StrEnum

from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  discord_id := <int64>$discord_id,
  player := (
    select waicolle::Player
    filter .client = global client and .user.discord_id = discord_id
  ),
select player {
  game_mode,
  moecoins,
  blood_shards,
  user: {
    discord_id,
    discord_id_str,
  },
}
"""


class WaicolleGameMode(StrEnum):
    WAIFU = 'WAIFU'
    HUSBANDO = 'HUSBANDO'
    ALL = 'ALL'


class PlayerGetByUserResultUser(BaseModel):
    discord_id: int
    discord_id_str: str


class PlayerGetByUserResult(BaseModel):
    game_mode: WaicolleGameMode
    moecoins: int
    blood_shards: int
    user: PlayerGetByUserResultUser


adapter = TypeAdapter(PlayerGetByUserResult | None)


async def player_get_by_user(
    executor: AsyncIOExecutor,
    *,
    discord_id: int,
) -> PlayerGetByUserResult | None:
    resp = await executor.query_single_json(
        EDGEQL_QUERY,
        discord_id=discord_id,
    )
    return adapter.validate_json(resp, strict=False)

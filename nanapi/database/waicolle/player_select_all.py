from enum import StrEnum

from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
select waicolle::Player {
  game_mode,
  moecoins,
  blood_shards,
  user: {
    discord_id,
    discord_id_str,
  },
}
filter .client = global client
"""


class WaicolleGameMode(StrEnum):
    WAIFU = 'WAIFU'
    HUSBANDO = 'HUSBANDO'
    ALL = 'ALL'


class PlayerSelectAllResultUser(BaseModel):
    discord_id: int
    discord_id_str: str


class PlayerSelectAllResult(BaseModel):
    game_mode: WaicolleGameMode
    moecoins: int
    blood_shards: int
    user: PlayerSelectAllResultUser


adapter = TypeAdapter(list[PlayerSelectAllResult])


async def player_select_all(
    executor: AsyncIOExecutor,
) -> list[PlayerSelectAllResult]:
    resp = await executor.query_json(
        EDGEQL_QUERY,
    )
    return adapter.validate_json(resp, strict=False)

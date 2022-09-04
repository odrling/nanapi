from datetime import datetime
from enum import StrEnum
from uuid import UUID

from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
select waicolle::Trade {
  id,
  player_a: {
    user: {
      discord_id,
      discord_id_str,
    },
  },
  waifus_a: {
    id,
    timestamp,
    level,
    locked,
    trade_locked,
    blooded,
    nanaed,
    custom_image,
    custom_name,
    custom_collage,
    custom_position,
    character: { id_al },
    owner: {
      user: {
        discord_id,
        discord_id_str,
      },
    },
    original_owner: {
      user: {
        discord_id,
        discord_id_str,
      },
    },
    custom_position_waifu: { id },
  },
  moecoins_a,
  blood_shards_a,
  player_b: {
    user: {
      discord_id,
      discord_id_str,
    },
  },
  waifus_b: {
    id,
    timestamp,
    level,
    locked,
    trade_locked,
    blooded,
    nanaed,
    custom_image,
    custom_name,
    custom_collage,
    custom_position,
    character: { id_al },
    owner: {
      user: {
        discord_id,
        discord_id_str,
      },
    },
    original_owner: {
      user: {
        discord_id,
        discord_id_str,
      },
    },
    custom_position_waifu: { id },
  },
  moecoins_b,
  blood_shards_b,
}
filter .client = global client
"""


class WaicolleCollagePosition(StrEnum):
    DEFAULT = 'DEFAULT'
    LEFT_OF = 'LEFT_OF'
    RIGHT_OF = 'RIGHT_OF'


class TradeSelectResultWaifusBCustomPositionWaifu(BaseModel):
    id: UUID


class TradeSelectResultWaifusBOriginalOwnerUser(BaseModel):
    discord_id: int
    discord_id_str: str


class TradeSelectResultWaifusBOriginalOwner(BaseModel):
    user: TradeSelectResultWaifusBOriginalOwnerUser


class TradeSelectResultWaifusBOwnerUser(BaseModel):
    discord_id: int
    discord_id_str: str


class TradeSelectResultWaifusBOwner(BaseModel):
    user: TradeSelectResultWaifusBOwnerUser


class TradeSelectResultWaifusBCharacter(BaseModel):
    id_al: int


class TradeSelectResultWaifusB(BaseModel):
    id: UUID
    timestamp: datetime
    level: int
    locked: bool
    trade_locked: bool
    blooded: bool
    nanaed: bool
    custom_image: str | None
    custom_name: str | None
    custom_collage: bool
    custom_position: WaicolleCollagePosition
    character: TradeSelectResultWaifusBCharacter
    owner: TradeSelectResultWaifusBOwner
    original_owner: TradeSelectResultWaifusBOriginalOwner | None
    custom_position_waifu: TradeSelectResultWaifusBCustomPositionWaifu | None


class TradeSelectResultPlayerBUser(BaseModel):
    discord_id: int
    discord_id_str: str


class TradeSelectResultPlayerB(BaseModel):
    user: TradeSelectResultPlayerBUser


class TradeSelectResultWaifusACustomPositionWaifu(BaseModel):
    id: UUID


class TradeSelectResultWaifusAOriginalOwnerUser(BaseModel):
    discord_id: int
    discord_id_str: str


class TradeSelectResultWaifusAOriginalOwner(BaseModel):
    user: TradeSelectResultWaifusAOriginalOwnerUser


class TradeSelectResultWaifusAOwnerUser(BaseModel):
    discord_id: int
    discord_id_str: str


class TradeSelectResultWaifusAOwner(BaseModel):
    user: TradeSelectResultWaifusAOwnerUser


class TradeSelectResultWaifusACharacter(BaseModel):
    id_al: int


class TradeSelectResultWaifusA(BaseModel):
    id: UUID
    timestamp: datetime
    level: int
    locked: bool
    trade_locked: bool
    blooded: bool
    nanaed: bool
    custom_image: str | None
    custom_name: str | None
    custom_collage: bool
    custom_position: WaicolleCollagePosition
    character: TradeSelectResultWaifusACharacter
    owner: TradeSelectResultWaifusAOwner
    original_owner: TradeSelectResultWaifusAOriginalOwner | None
    custom_position_waifu: TradeSelectResultWaifusACustomPositionWaifu | None


class TradeSelectResultPlayerAUser(BaseModel):
    discord_id: int
    discord_id_str: str


class TradeSelectResultPlayerA(BaseModel):
    user: TradeSelectResultPlayerAUser


class TradeSelectResult(BaseModel):
    id: UUID
    player_a: TradeSelectResultPlayerA
    waifus_a: list[TradeSelectResultWaifusA]
    moecoins_a: int
    blood_shards_a: int
    player_b: TradeSelectResultPlayerB
    waifus_b: list[TradeSelectResultWaifusB]
    moecoins_b: int
    blood_shards_b: int


adapter = TypeAdapter(list[TradeSelectResult])


async def trade_select(
    executor: AsyncIOExecutor,
) -> list[TradeSelectResult]:
    resp = await executor.query_json(
        EDGEQL_QUERY,
    )
    return adapter.validate_json(resp, strict=False)

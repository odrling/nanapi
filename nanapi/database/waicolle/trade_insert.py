from datetime import datetime
from enum import StrEnum
from uuid import UUID

from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  player_a_discord_id := <int64>$player_a_discord_id,
  waifus_a_ids := <array<uuid>>$waifus_a_ids,
  moecoins_a := <optional int32>$moecoins_a ?? 0,
  blood_shards_a := <optional int32>$blood_shards_a ?? 0,
  player_b_discord_id := <int64>$player_b_discord_id,
  waifus_b_ids := <array<uuid>>$waifus_b_ids,
  moecoins_b := <optional int32>$moecoins_b ?? 0,
  blood_shards_b := <optional int32>$blood_shards_b ?? 0,
  player_a := (select waicolle::Player filter .client = global client and .user.discord_id = player_a_discord_id),
  player_b := (select waicolle::Player filter .client = global client and .user.discord_id = player_b_discord_id),
  inserted := (
    insert waicolle::Trade {
      client := global client,
      player_a := player_a,
      waifus_a := (select waicolle::Waifu filter .id in array_unpack(waifus_a_ids)),
      moecoins_a := moecoins_a,
      blood_shards_a := blood_shards_a,
      player_b := player_b,
      waifus_b := (select waicolle::Waifu filter .id in array_unpack(waifus_b_ids)),
      moecoins_b := moecoins_b,
      blood_shards_b := blood_shards_b,
    }
  )
select inserted {
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
"""


class WaicolleCollagePosition(StrEnum):
    DEFAULT = 'DEFAULT'
    LEFT_OF = 'LEFT_OF'
    RIGHT_OF = 'RIGHT_OF'


class TradeInsertResultWaifusBCustomPositionWaifu(BaseModel):
    id: UUID


class TradeInsertResultWaifusBOriginalOwnerUser(BaseModel):
    discord_id: int
    discord_id_str: str


class TradeInsertResultWaifusBOriginalOwner(BaseModel):
    user: TradeInsertResultWaifusBOriginalOwnerUser


class TradeInsertResultWaifusBOwnerUser(BaseModel):
    discord_id: int
    discord_id_str: str


class TradeInsertResultWaifusBOwner(BaseModel):
    user: TradeInsertResultWaifusBOwnerUser


class TradeInsertResultWaifusBCharacter(BaseModel):
    id_al: int


class TradeInsertResultWaifusB(BaseModel):
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
    character: TradeInsertResultWaifusBCharacter
    owner: TradeInsertResultWaifusBOwner
    original_owner: TradeInsertResultWaifusBOriginalOwner | None
    custom_position_waifu: TradeInsertResultWaifusBCustomPositionWaifu | None


class TradeInsertResultPlayerBUser(BaseModel):
    discord_id: int
    discord_id_str: str


class TradeInsertResultPlayerB(BaseModel):
    user: TradeInsertResultPlayerBUser


class TradeInsertResultWaifusACustomPositionWaifu(BaseModel):
    id: UUID


class TradeInsertResultWaifusAOriginalOwnerUser(BaseModel):
    discord_id: int
    discord_id_str: str


class TradeInsertResultWaifusAOriginalOwner(BaseModel):
    user: TradeInsertResultWaifusAOriginalOwnerUser


class TradeInsertResultWaifusAOwnerUser(BaseModel):
    discord_id: int
    discord_id_str: str


class TradeInsertResultWaifusAOwner(BaseModel):
    user: TradeInsertResultWaifusAOwnerUser


class TradeInsertResultWaifusACharacter(BaseModel):
    id_al: int


class TradeInsertResultWaifusA(BaseModel):
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
    character: TradeInsertResultWaifusACharacter
    owner: TradeInsertResultWaifusAOwner
    original_owner: TradeInsertResultWaifusAOriginalOwner | None
    custom_position_waifu: TradeInsertResultWaifusACustomPositionWaifu | None


class TradeInsertResultPlayerAUser(BaseModel):
    discord_id: int
    discord_id_str: str


class TradeInsertResultPlayerA(BaseModel):
    user: TradeInsertResultPlayerAUser


class TradeInsertResult(BaseModel):
    id: UUID
    player_a: TradeInsertResultPlayerA
    waifus_a: list[TradeInsertResultWaifusA]
    moecoins_a: int
    blood_shards_a: int
    player_b: TradeInsertResultPlayerB
    waifus_b: list[TradeInsertResultWaifusB]
    moecoins_b: int
    blood_shards_b: int


adapter = TypeAdapter(TradeInsertResult)


async def trade_insert(
    executor: AsyncIOExecutor,
    *,
    player_a_discord_id: int,
    waifus_a_ids: list[UUID],
    player_b_discord_id: int,
    waifus_b_ids: list[UUID],
    moecoins_a: int | None = None,
    blood_shards_a: int | None = None,
    moecoins_b: int | None = None,
    blood_shards_b: int | None = None,
) -> TradeInsertResult:
    resp = await executor.query_single_json(
        EDGEQL_QUERY,
        player_a_discord_id=player_a_discord_id,
        waifus_a_ids=waifus_a_ids,
        player_b_discord_id=player_b_discord_id,
        waifus_b_ids=waifus_b_ids,
        moecoins_a=moecoins_a,
        blood_shards_a=blood_shards_a,
        moecoins_b=moecoins_b,
        blood_shards_b=blood_shards_b,
    )
    return adapter.validate_json(resp, strict=False)

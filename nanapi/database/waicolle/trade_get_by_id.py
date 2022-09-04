from uuid import UUID

from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  id := <uuid>$id,
select waicolle::Trade {
  id,
  player_a: {
    user: {
      discord_id,
      discord_id_str,
    },
  },
  waifus_a,
  moecoins_a,
  blood_shards_a,
  player_b: {
    user: {
      discord_id,
      discord_id_str,
    },
  },
  waifus_b,
  moecoins_b,
  blood_shards_b,
}
filter .id = id
"""


class TradeGetByIdResultWaifusB(BaseModel):
    id: UUID


class TradeGetByIdResultPlayerBUser(BaseModel):
    discord_id: int
    discord_id_str: str


class TradeGetByIdResultPlayerB(BaseModel):
    user: TradeGetByIdResultPlayerBUser


class TradeGetByIdResultWaifusA(BaseModel):
    id: UUID


class TradeGetByIdResultPlayerAUser(BaseModel):
    discord_id: int
    discord_id_str: str


class TradeGetByIdResultPlayerA(BaseModel):
    user: TradeGetByIdResultPlayerAUser


class TradeGetByIdResult(BaseModel):
    id: UUID
    player_a: TradeGetByIdResultPlayerA
    waifus_a: list[TradeGetByIdResultWaifusA]
    moecoins_a: int
    blood_shards_a: int
    player_b: TradeGetByIdResultPlayerB
    waifus_b: list[TradeGetByIdResultWaifusB]
    moecoins_b: int
    blood_shards_b: int


adapter = TypeAdapter(TradeGetByIdResult | None)


async def trade_get_by_id(
    executor: AsyncIOExecutor,
    *,
    id: UUID,
) -> TradeGetByIdResult | None:
    resp = await executor.query_single_json(
        EDGEQL_QUERY,
        id=id,
    )
    return adapter.validate_json(resp, strict=False)

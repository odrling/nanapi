from datetime import datetime
from enum import StrEnum
from uuid import UUID

from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  ids := <array<uuid>>$ids,
select waicolle::Waifu {
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
}
filter .id in array_unpack(ids)
"""


class WaicolleCollagePosition(StrEnum):
    DEFAULT = 'DEFAULT'
    LEFT_OF = 'LEFT_OF'
    RIGHT_OF = 'RIGHT_OF'


class WaifuSelectResultCustomPositionWaifu(BaseModel):
    id: UUID


class WaifuSelectResultOriginalOwnerUser(BaseModel):
    discord_id: int
    discord_id_str: str


class WaifuSelectResultOriginalOwner(BaseModel):
    user: WaifuSelectResultOriginalOwnerUser


class WaifuSelectResultOwnerUser(BaseModel):
    discord_id: int
    discord_id_str: str


class WaifuSelectResultOwner(BaseModel):
    user: WaifuSelectResultOwnerUser


class WaifuSelectResultCharacter(BaseModel):
    id_al: int


class WaifuSelectResult(BaseModel):
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
    character: WaifuSelectResultCharacter
    owner: WaifuSelectResultOwner
    original_owner: WaifuSelectResultOriginalOwner | None
    custom_position_waifu: WaifuSelectResultCustomPositionWaifu | None


adapter = TypeAdapter(list[WaifuSelectResult])


async def waifu_select(
    executor: AsyncIOExecutor,
    *,
    ids: list[UUID],
) -> list[WaifuSelectResult]:
    resp = await executor.query_json(
        EDGEQL_QUERY,
        ids=ids,
    )
    return adapter.validate_json(resp, strict=False)

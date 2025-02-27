from uuid import UUID

from gel import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  discord_id := <int64>$discord_id,
  player := (select waicolle::Player filter .client = global client and .user.discord_id = discord_id),
select assert_exists(player) {
  tracked_medias := .tracked_items[is anilist::Media] {
    id_al,
  },
  tracked_staffs := .tracked_items[is anilist::Staff] {
    id_al,
  },
  tracked_collections: {
    id,
  },
}
"""


class PlayerTrackedItemsResultTrackedCollections(BaseModel):
    id: UUID


class PlayerTrackedItemsResultTrackedStaffs(BaseModel):
    id_al: int


class PlayerTrackedItemsResultTrackedMedias(BaseModel):
    id_al: int


class PlayerTrackedItemsResult(BaseModel):
    tracked_medias: list[PlayerTrackedItemsResultTrackedMedias]
    tracked_staffs: list[PlayerTrackedItemsResultTrackedStaffs]
    tracked_collections: list[PlayerTrackedItemsResultTrackedCollections]


adapter = TypeAdapter(PlayerTrackedItemsResult)


async def player_tracked_items(
    executor: AsyncIOExecutor,
    *,
    discord_id: int,
) -> PlayerTrackedItemsResult:
    resp = await executor.query_single_json(
        EDGEQL_QUERY,
        discord_id=discord_id,
    )
    return adapter.validate_json(resp, strict=False)

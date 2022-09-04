from uuid import UUID

from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  id := <uuid>$id,
  id_al := <int32>$id_al,
  staff := (select anilist::Staff filter .id_al = id_al),
update waicolle::Collection
filter .id = id
set {
  items -= staff,
}
"""


class CollectionRemoveStaffResult(BaseModel):
    id: UUID


adapter = TypeAdapter(CollectionRemoveStaffResult | None)


async def collection_remove_staff(
    executor: AsyncIOExecutor,
    *,
    id: UUID,
    id_al: int,
) -> CollectionRemoveStaffResult | None:
    resp = await executor.query_single_json(
        EDGEQL_QUERY,
        id=id,
        id_al=id_al,
    )
    return adapter.validate_json(resp, strict=False)

from typing import Any

import orjson
from gel import AsyncIOExecutor

EDGEQL_QUERY = r"""
with
  tags := <json>$tags,
for tag in json_array_unpack(tags) union (
  with
    id_al := <int32>json_get(tag, 'id_al'),
    name := <str>json_get(tag, 'name'),
    description := <str>json_get(tag, 'description'),
    category := <str>json_get(tag, 'category'),
    is_adult := <bool>json_get(tag, 'is_adult'),
  insert anilist::Tag {
    id_al := id_al,
    name := name,
    description := description,
    category := category,
    is_adult := is_adult,
  }
  unless conflict on .id_al
  else (
    update anilist::Tag set {
      name := name,
      description := description,
      category := category,
      is_adult := is_adult,
    }
  )
)
"""


async def tag_merge_multiple(
    executor: AsyncIOExecutor,
    *,
    tags: Any,
) -> None:
    await executor.query_json(
        EDGEQL_QUERY,
        tags=orjson.dumps(tags).decode(),
    )

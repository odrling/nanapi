from uuid import UUID

from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  url := <str>$url,
  data := <str>$data,
insert anilist::Image {
  url := url,
  data := data,
}
unless conflict;
"""


class ImageSaveResult(BaseModel):
    id: UUID


adapter = TypeAdapter(ImageSaveResult | None)


async def image_save(
    executor: AsyncIOExecutor,
    *,
    url: str,
    data: str,
) -> ImageSaveResult | None:
    resp = await executor.query_single_json(
        EDGEQL_QUERY,
        url=url,
        data=data,
    )
    return adapter.validate_json(resp, strict=False)

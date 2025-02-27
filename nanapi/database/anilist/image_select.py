from gel import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  urls := <array<str>>$urls,
select anilist::Image {
  url,
  data,
}
filter .url in array_unpack(urls)
"""


class ImageSelectResult(BaseModel):
    url: str
    data: str


adapter = TypeAdapter(list[ImageSelectResult])


async def image_select(
    executor: AsyncIOExecutor,
    *,
    urls: list[str],
) -> list[ImageSelectResult]:
    resp = await executor.query_json(
        EDGEQL_QUERY,
        urls=urls,
    )
    return adapter.validate_json(resp, strict=False)

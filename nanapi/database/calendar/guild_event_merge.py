from datetime import datetime
from uuid import UUID

from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  discord_id := <int64>$discord_id,
  name := <str>$name,
  description := <optional str>$description,
  location := <optional str>$location,
  start_time := <datetime>$start_time,
  end_time := <datetime>$end_time,
  image := <optional str>$image,
  url := <optional str>$url,
  organizer_id := <int64>$organizer_id,
  organizer_username := <str>$organizer_username,
  organizer := (
    insert user::User {
      discord_id := organizer_id,
      discord_username := organizer_username,
    }
    unless conflict on .discord_id
    else (
      update user::User set {
        discord_username := organizer_username,
      }
    )
  ),
insert calendar::GuildEvent {
  client := global client,
  discord_id := discord_id,
  name := name,
  description := description,
  location := location,
  start_time := start_time,
  end_time := end_time,
  image := image,
  url := url,
  organizer := organizer,
}
unless conflict on ((.client, .discord_id))
else (
  update calendar::GuildEvent set {
    name := name,
    description := description,
    location := location,
    start_time := start_time,
    end_time := end_time,
    image := image,
    url := url,
    organizer := organizer,
  }
)
"""


class GuildEventMergeResult(BaseModel):
    id: UUID


adapter = TypeAdapter(GuildEventMergeResult | None)


async def guild_event_merge(
    executor: AsyncIOExecutor,
    *,
    discord_id: int,
    name: str,
    start_time: datetime,
    end_time: datetime,
    organizer_id: int,
    organizer_username: str,
    description: str | None = None,
    location: str | None = None,
    image: str | None = None,
    url: str | None = None,
) -> GuildEventMergeResult | None:
    resp = await executor.query_single_json(
        EDGEQL_QUERY,
        discord_id=discord_id,
        name=name,
        start_time=start_time,
        end_time=end_time,
        organizer_id=organizer_id,
        organizer_username=organizer_username,
        description=description,
        location=location,
        image=image,
        url=url,
    )
    return adapter.validate_json(resp, strict=False)

from datetime import datetime
from enum import StrEnum
from typing import Literal
from uuid import UUID

from edgedb import AsyncIOExecutor
from pydantic import BaseModel, Field, TypeAdapter

EDGEQL_QUERY = r"""
with
  id := <optional uuid>$id,
  status := <optional projection::Status>$status,
  message_id := <optional int64>$message_id,
  channel_id := <optional int64>$channel_id,
  all_projos := (select projection::Projection filter .client = global client),
  filtered := (
    (select all_projos filter .id = id)
    if exists id else
    (select all_projos filter .status = status and .channel_id = channel_id)
    if exists status and exists channel_id else
    (select all_projos filter .status = status)
    if exists status else
    (select all_projos filter .message_id = message_id)
    if exists message_id else
    (select all_projos filter .channel_id = channel_id)
    if exists channel_id else
    (select all_projos)
  )
select filtered {
  id,
  name,
  status,
  message_id,
  message_id_str,
  channel_id,
  channel_id_str,
  medias: {
    id_al,
    title_user_preferred,
    @added,
  } order by @added,
  external_medias: {
    id,
    title,
    @added,
  } order by @added,
  events: {
    date,
    description,
  }
}
"""


PROJO_SELECT_STATUS = Literal[
    'ONGOING',
    'COMPLETED',
]


class ProjectionStatus(StrEnum):
    ONGOING = 'ONGOING'
    COMPLETED = 'COMPLETED'


class ProjoSelectResultEvents(BaseModel):
    date: datetime
    description: str


class ProjoSelectResultExternalMedias(BaseModel):
    id: UUID
    title: str
    link_added: datetime | None = Field(alias='@added')


class ProjoSelectResultMedias(BaseModel):
    id_al: int
    title_user_preferred: str
    link_added: datetime | None = Field(alias='@added')


class ProjoSelectResult(BaseModel):
    id: UUID
    name: str
    status: ProjectionStatus
    message_id: int | None
    message_id_str: str | None
    channel_id: int
    channel_id_str: str
    medias: list[ProjoSelectResultMedias]
    external_medias: list[ProjoSelectResultExternalMedias]
    events: list[ProjoSelectResultEvents]


adapter = TypeAdapter(list[ProjoSelectResult])


async def projo_select(
    executor: AsyncIOExecutor,
    *,
    id: UUID | None = None,
    status: PROJO_SELECT_STATUS | None = None,
    message_id: int | None = None,
    channel_id: int | None = None,
) -> list[ProjoSelectResult]:
    resp = await executor.query_json(
        EDGEQL_QUERY,
        id=id,
        status=status,
        message_id=message_id,
        channel_id=channel_id,
    )
    return adapter.validate_json(resp, strict=False)

from typing import Any
from uuid import UUID

import orjson
from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  message_id := <int64>$message_id,
  channel_id := <int64>$channel_id,
  question := <str>$question,
  options := <json>$options,
  _poll := (
    insert poll::Poll {
      client := global client,
      message_id := message_id,
      channel_id := channel_id,
      question := question,
    }
  ),
  _options := (
    for option in json_array_unpack(options) union (
      with
        rank := <int32>json_get(option, 'rank'),
        text := <str>json_get(option, 'text'),
      insert poll::Option {
        client := global client,
        rank := rank,
        text := text,
        poll := _poll
      }
    )
  ),
select { _poll, _options }
"""


class PollInsertResult(BaseModel):
    id: UUID


adapter = TypeAdapter(list[PollInsertResult])


async def poll_insert(
    executor: AsyncIOExecutor,
    *,
    message_id: int,
    channel_id: int,
    question: str,
    options: Any,
) -> list[PollInsertResult]:
    resp = await executor.query_json(
        EDGEQL_QUERY,
        message_id=message_id,
        channel_id=channel_id,
        question=question,
        options=orjson.dumps(options).decode(),
    )
    return adapter.validate_json(resp, strict=False)

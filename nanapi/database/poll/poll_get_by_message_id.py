from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  message_id := <int64>$message_id,
select poll::Poll {
  message_id,
  message_id_str,
  channel_id,
  channel_id_str,
  question,
  options: {
    rank,
    text,
    votes: {
      user: {
        discord_id,
        discord_id_str,
      }
    }
  }
}
filter .message_id = message_id
"""


class PollGetByMessageIdResultOptionsVotesUser(BaseModel):
    discord_id: int
    discord_id_str: str


class PollGetByMessageIdResultOptionsVotes(BaseModel):
    user: PollGetByMessageIdResultOptionsVotesUser


class PollGetByMessageIdResultOptions(BaseModel):
    rank: int
    text: str
    votes: list[PollGetByMessageIdResultOptionsVotes]


class PollGetByMessageIdResult(BaseModel):
    message_id: int
    message_id_str: str
    channel_id: int
    channel_id_str: str
    question: str
    options: list[PollGetByMessageIdResultOptions]


adapter = TypeAdapter(PollGetByMessageIdResult | None)


async def poll_get_by_message_id(
    executor: AsyncIOExecutor,
    *,
    message_id: int,
) -> PollGetByMessageIdResult | None:
    resp = await executor.query_single_json(
        EDGEQL_QUERY,
        message_id=message_id,
    )
    return adapter.validate_json(resp, strict=False)

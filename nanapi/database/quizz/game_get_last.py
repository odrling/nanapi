from datetime import datetime
from enum import StrEnum
from uuid import UUID

from gel import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  channel_id := <int64>$channel_id,
select quizz::Game {
  id,
  status,
  message_id,
  message_id_str,
  answer_bananed,
  started_at,
  ended_at,
  winner: {
    discord_id,
    discord_id_str,
  },
  quizz: {
    id,
    channel_id,
    channel_id_str,
    description,
    url,
    is_image,
    answer,
    answer_source,
    submitted_at,
    hikaried,
    author: {
      discord_id,
      discord_id_str,
    },
  }
}
filter .client = global client and .quizz.channel_id = channel_id and .status = quizz::Status.ENDED
order by .ended_at desc
limit 1
"""


class QuizzStatus(StrEnum):
    STARTED = 'STARTED'
    ENDED = 'ENDED'


class GameGetLastResultQuizzAuthor(BaseModel):
    discord_id: int
    discord_id_str: str


class GameGetLastResultQuizz(BaseModel):
    id: UUID
    channel_id: int
    channel_id_str: str
    description: str | None
    url: str | None
    is_image: bool
    answer: str | None
    answer_source: str | None
    submitted_at: datetime
    hikaried: bool | None
    author: GameGetLastResultQuizzAuthor


class GameGetLastResultWinner(BaseModel):
    discord_id: int
    discord_id_str: str


class GameGetLastResult(BaseModel):
    id: UUID
    status: QuizzStatus
    message_id: int
    message_id_str: str
    answer_bananed: str | None
    started_at: datetime
    ended_at: datetime | None
    winner: GameGetLastResultWinner | None
    quizz: GameGetLastResultQuizz


adapter = TypeAdapter(GameGetLastResult | None)


async def game_get_last(
    executor: AsyncIOExecutor,
    *,
    channel_id: int,
) -> GameGetLastResult | None:
    resp = await executor.query_single_json(
        EDGEQL_QUERY,
        channel_id=channel_id,
    )
    return adapter.validate_json(resp, strict=False)

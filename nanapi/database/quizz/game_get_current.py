from datetime import datetime
from enum import StrEnum
from uuid import UUID

from gel import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  channel_id := <int64>$channel_id,
  games := (
    select quizz::Game
    filter .client = global client and .quizz.channel_id = channel_id and .status = quizz::Status.STARTED
  )
select assert_single(games) {
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
"""


class QuizzStatus(StrEnum):
    STARTED = 'STARTED'
    ENDED = 'ENDED'


class GameGetCurrentResultQuizzAuthor(BaseModel):
    discord_id: int
    discord_id_str: str


class GameGetCurrentResultQuizz(BaseModel):
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
    author: GameGetCurrentResultQuizzAuthor


class GameGetCurrentResultWinner(BaseModel):
    discord_id: int
    discord_id_str: str


class GameGetCurrentResult(BaseModel):
    id: UUID
    status: QuizzStatus
    message_id: int
    message_id_str: str
    answer_bananed: str | None
    started_at: datetime
    ended_at: datetime | None
    winner: GameGetCurrentResultWinner | None
    quizz: GameGetCurrentResultQuizz


adapter = TypeAdapter(GameGetCurrentResult | None)


async def game_get_current(
    executor: AsyncIOExecutor,
    *,
    channel_id: int,
) -> GameGetCurrentResult | None:
    resp = await executor.query_single_json(
        EDGEQL_QUERY,
        channel_id=channel_id,
    )
    return adapter.validate_json(resp, strict=False)

from datetime import datetime
from enum import StrEnum
from uuid import UUID

from gel import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  id := <uuid>$id,
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
filter .id = id
"""


class QuizzStatus(StrEnum):
    STARTED = 'STARTED'
    ENDED = 'ENDED'


class GameGetByIdResultQuizzAuthor(BaseModel):
    discord_id: int
    discord_id_str: str


class GameGetByIdResultQuizz(BaseModel):
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
    author: GameGetByIdResultQuizzAuthor


class GameGetByIdResultWinner(BaseModel):
    discord_id: int
    discord_id_str: str


class GameGetByIdResult(BaseModel):
    id: UUID
    status: QuizzStatus
    message_id: int
    message_id_str: str
    answer_bananed: str | None
    started_at: datetime
    ended_at: datetime | None
    winner: GameGetByIdResultWinner | None
    quizz: GameGetByIdResultQuizz


adapter = TypeAdapter(GameGetByIdResult | None)


async def game_get_by_id(
    executor: AsyncIOExecutor,
    *,
    id: UUID,
) -> GameGetByIdResult | None:
    resp = await executor.query_single_json(
        EDGEQL_QUERY,
        id=id,
    )
    return adapter.validate_json(resp, strict=False)

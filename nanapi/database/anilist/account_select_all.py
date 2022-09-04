from enum import StrEnum

from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
select anilist::Account {
  service,
  username,
  user: {
    discord_id,
    discord_id_str,
  },
}
"""


class AnilistService(StrEnum):
    ANILIST = 'ANILIST'
    MYANIMELIST = 'MYANIMELIST'


class AccountSelectAllResultUser(BaseModel):
    discord_id: int
    discord_id_str: str


class AccountSelectAllResult(BaseModel):
    service: AnilistService
    username: str
    user: AccountSelectAllResultUser


adapter = TypeAdapter(list[AccountSelectAllResult])


async def account_select_all(
    executor: AsyncIOExecutor,
) -> list[AccountSelectAllResult]:
    resp = await executor.query_json(
        EDGEQL_QUERY,
    )
    return adapter.validate_json(resp, strict=False)

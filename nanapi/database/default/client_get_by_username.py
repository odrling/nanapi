from uuid import UUID

from gel import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  username := <str>$username,
select Client {
  id,
  username,
  password_hash,
}
filter .username = username
"""


class ClientGetByUsernameResult(BaseModel):
    id: UUID
    username: str
    password_hash: str


adapter = TypeAdapter(ClientGetByUsernameResult | None)


async def client_get_by_username(
    executor: AsyncIOExecutor,
    *,
    username: str,
) -> ClientGetByUsernameResult | None:
    resp = await executor.query_single_json(
        EDGEQL_QUERY,
        username=username,
    )
    return adapter.validate_json(resp, strict=False)

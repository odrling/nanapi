from uuid import UUID

from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  username := <str>$username,
  password_hash := <str>$password_hash,
insert Client {
  username := username,
  password_hash := password_hash,
}
"""


class ClientInsertResult(BaseModel):
    id: UUID


adapter = TypeAdapter(ClientInsertResult)


async def client_insert(
    executor: AsyncIOExecutor,
    *,
    username: str,
    password_hash: str,
) -> ClientInsertResult:
    resp = await executor.query_single_json(
        EDGEQL_QUERY,
        username=username,
        password_hash=password_hash,
    )
    return adapter.validate_json(resp, strict=False)

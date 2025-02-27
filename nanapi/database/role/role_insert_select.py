from gel import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  role_id := <int64>$role_id,
  emoji := <str>$emoji,
  role := (
    insert role::Role {
      client := global client,
      role_id := role_id,
      emoji := emoji,
    }
  )
select role {
  role_id,
  role_id_str,
  emoji,
}
"""


class RoleInsertSelectResult(BaseModel):
    role_id: int
    role_id_str: str
    emoji: str


adapter = TypeAdapter(RoleInsertSelectResult)


async def role_insert_select(
    executor: AsyncIOExecutor,
    *,
    role_id: int,
    emoji: str,
) -> RoleInsertSelectResult:
    resp = await executor.query_single_json(
        EDGEQL_QUERY,
        role_id=role_id,
        emoji=emoji,
    )
    return adapter.validate_json(resp, strict=False)

from gel import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
select role::Role {
  role_id,
  role_id_str,
  emoji
}
filter .client = global client
"""


class RoleSelectAllResult(BaseModel):
    role_id: int
    role_id_str: str
    emoji: str


adapter = TypeAdapter(list[RoleSelectAllResult])


async def role_select_all(
    executor: AsyncIOExecutor,
) -> list[RoleSelectAllResult]:
    resp = await executor.query_json(
        EDGEQL_QUERY,
    )
    return adapter.validate_json(resp, strict=False)

from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
select anilist::Staff { id_al }
"""


class StaffSelectAllIdsResult(BaseModel):
    id_al: int


adapter = TypeAdapter(list[StaffSelectAllIdsResult])


async def staff_select_all_ids(
    executor: AsyncIOExecutor,
) -> list[StaffSelectAllIdsResult]:
    resp = await executor.query_json(
        EDGEQL_QUERY,
    )
    return adapter.validate_json(resp, strict=False)

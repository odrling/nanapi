from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
select amq::Setting { key, value }
filter .client = global client
"""


class SettingsSelectAllResult(BaseModel):
    key: str
    value: str


adapter = TypeAdapter(list[SettingsSelectAllResult])


async def settings_select_all(
    executor: AsyncIOExecutor,
) -> list[SettingsSelectAllResult]:
    resp = await executor.query_json(
        EDGEQL_QUERY,
    )
    return adapter.validate_json(resp, strict=False)

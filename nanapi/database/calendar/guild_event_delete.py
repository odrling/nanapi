from uuid import UUID

from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
with
  discord_id := <int64>$discord_id
delete calendar::GuildEvent
filter .client = global client and .discord_id = discord_id
"""


class GuildEventDeleteResult(BaseModel):
    id: UUID


adapter = TypeAdapter(GuildEventDeleteResult | None)


async def guild_event_delete(
    executor: AsyncIOExecutor,
    *,
    discord_id: int,
) -> GuildEventDeleteResult | None:
    resp = await executor.query_single_json(
        EDGEQL_QUERY,
        discord_id=discord_id,
    )
    return adapter.validate_json(resp, strict=False)

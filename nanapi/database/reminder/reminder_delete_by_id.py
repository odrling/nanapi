from uuid import UUID

from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
delete reminder::Reminder filter .id = <uuid>$id;
"""


class ReminderDeleteByIdResult(BaseModel):
    id: UUID


adapter = TypeAdapter(ReminderDeleteByIdResult | None)


async def reminder_delete_by_id(
    executor: AsyncIOExecutor,
    *,
    id: UUID,
) -> ReminderDeleteByIdResult | None:
    resp = await executor.query_single_json(
        EDGEQL_QUERY,
        id=id,
    )
    return adapter.validate_json(resp, strict=False)

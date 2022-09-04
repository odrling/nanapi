from edgedb import AsyncIOExecutor
from pydantic import BaseModel, TypeAdapter

EDGEQL_QUERY = r"""
select waicolle::Coupon {
  code,
  claimed_by: {
    user: {
      discord_id,
      discord_id_str,
    },
  },
}
filter .client = global client
"""


class CouponSelectAllResultClaimedByUser(BaseModel):
    discord_id: int
    discord_id_str: str


class CouponSelectAllResultClaimedBy(BaseModel):
    user: CouponSelectAllResultClaimedByUser


class CouponSelectAllResult(BaseModel):
    code: str
    claimed_by: list[CouponSelectAllResultClaimedBy]


adapter = TypeAdapter(list[CouponSelectAllResult])


async def coupon_select_all(
    executor: AsyncIOExecutor,
) -> list[CouponSelectAllResult]:
    resp = await executor.query_json(
        EDGEQL_QUERY,
    )
    return adapter.validate_json(resp, strict=False)

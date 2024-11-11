from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud.user import get_users_by_referrer_id
from app.schemas import UserResponseSchema


async def get_referrals_by_referrer_id(
        db: AsyncSession,
        referrer_id: int,
) -> Sequence[UserResponseSchema]:
    referrals = await get_users_by_referrer_id(db, referrer_id)
    return [UserResponseSchema.from_orm(referral) for referral in referrals]

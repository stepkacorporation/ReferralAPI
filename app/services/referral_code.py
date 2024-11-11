from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud.referral_code import get_referral_code_by_user_id
from app.database.crud.user import get_user_by_email
from app.schemas import ReferralCodeResponseSchema


async def get_referral_code_by_email(
        db: AsyncSession,
        email: str,
) -> ReferralCodeResponseSchema | None:
    user = await get_user_by_email(db, email)

    if not user:
        return None

    referral_code = await get_referral_code_by_user_id(db, user.id)

    if referral_code:
        return ReferralCodeResponseSchema.from_orm(referral_code)

    return None
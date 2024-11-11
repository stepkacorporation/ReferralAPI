from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import ReferralCode
from app.schemas import ReferralCodeCreateSchema


async def create_referral_code(
        db: AsyncSession,
        referral_code_create_schema: ReferralCodeCreateSchema,
) -> ReferralCode:
    referral_code = ReferralCode(
        code=referral_code_create_schema.code,
        user_id=referral_code_create_schema.user_id,
        expiry_date=referral_code_create_schema.expiry_date,
    )
    db.add(referral_code)
    await db.commit()
    await db.refresh(referral_code)
    return referral_code


async def get_referral_code_by_id(
        db: AsyncSession,
        referral_code_id: int,
) -> ReferralCode | None:
    return await db.get(ReferralCode, referral_code_id)


async def get_referral_code_by_user_id(
        db: AsyncSession,
        user_id: int,
) -> ReferralCode | None:
    return await db.scalar(select(ReferralCode).where(ReferralCode.user_id == user_id))


async def delete_referral_code(
        db: AsyncSession,
        referral_code_id: int,
) -> bool:
    referral_code = await get_referral_code_by_id(db, referral_code_id)

    if referral_code:
        await db.delete(referral_code)
        await db.commit()
        return True

    return False

from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud.referral_code import get_referral_code_by_user_id
from app.database.crud.user import get_users_by_referrer_id, create_user, get_user_by_referral_code
from app.database.models import User
from app.schemas import UserResponseSchema, UserCreateSchema


async def get_referrals_by_referrer_id(
        db: AsyncSession,
        referrer_id: int,
) -> Sequence[UserResponseSchema]:
    referrals = await get_users_by_referrer_id(db, referrer_id)
    return [UserResponseSchema.from_orm(referral) for referral in referrals]


async def create_user_with_referral(
        db: AsyncSession,
        user_create_schema: UserCreateSchema,
) -> User:
    referred_by = None
    if user_create_schema.referral_code:
        referring_user = await get_user_by_referral_code(db, user_create_schema.referral_code)
        if not referring_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Invalid referral code'
            )

        referral_code = await get_referral_code_by_user_id(db, referring_user.id)
        if referral_code and not referral_code.is_active():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Referral code has expired'
            )

        referred_by = referring_user.id

    return await create_user(db, user_create_schema, referred_by)

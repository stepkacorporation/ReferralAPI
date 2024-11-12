from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User
from app.schemas import UserCreateSchema
from app.utils.security import hash_password


async def create_user(
        db: AsyncSession,
        user_create_schema: UserCreateSchema,
        referred_by: int | None = None,
) -> User:
    password_hash = hash_password(user_create_schema.password)

    user = User(
        email=user_create_schema.email,
        password_hash=password_hash,
        referred_by=referred_by
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_user_by_id(
        db: AsyncSession,
        user_id: int,
) -> User | None:
    return await db.get(User, user_id)


async def get_user_by_email(
        db: AsyncSession,
        email: str
) -> User | None:
    return await db.scalar(select(User).where(User.email == email))


async def get_user_by_referral_code(
        db: AsyncSession,
        referral_code: str,
) -> User | None:
    return await db.scalar(select(User).where(User.referral_code.has(code=referral_code)))


async def get_users_by_referrer_id(
        db: AsyncSession,
        referrer_id: int,
) -> Sequence[User]:
    referrals_query = await db.scalars(select(User).where(User.referred_by == referrer_id))
    return referrals_query.all()

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User
from app.schemas import UserCreateSchema


async def create_user(
        db: AsyncSession,
        user_create_schema: UserCreateSchema,
) -> User:
    user = User(
        email=user_create_schema.email,
        password_hash=user_create_schema.password_hash,
        referral_code=user_create_schema.ref
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_user_by_email(
        db: AsyncSession,
        email: str
) -> User | None:
    return await db.scalar(select(User).where(User.email == email))


async def get_users_by_referrer_id(
        db: AsyncSession,
        referrer_id: int,
) -> Sequence[User]:
    referrals_query = await db.scalars(select(User).where(User.referred_by == referrer_id))
    return referrals_query.all()

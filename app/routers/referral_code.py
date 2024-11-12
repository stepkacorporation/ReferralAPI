from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.cache import cache
from app.database import get_db
from app.database.crud.referral_code import get_referral_code_by_user_id, create_referral_code, delete_referral_code
from app.schemas import (
    UserResponseSchema,
    ReferralCodeResponseSchema,
    ReferralCodeCreateSchema,
)
from app.services.auth import get_user_id_from_token
from app.services.referral_code import get_referral_code_by_email
from app.services.user import get_referrals_by_referrer_id

router = APIRouter(tags=['referral-system'])


@router.post(
    '/ref/create',
    status_code=status.HTTP_201_CREATED,
    summary='Create a referral code',
    description='This endpoint allows an authenticated user to create a new referral code. '
                'A user can only have one referral code at a time, and it must be created'
                ' with an expiration date.'
)
async def create_ref_code(
        db: Annotated[AsyncSession, Depends(get_db)],
        user_id: Annotated[int, Depends(get_user_id_from_token)],
        referral_code_create_schema: ReferralCodeCreateSchema
) -> ReferralCodeResponseSchema:
    existing_code = await get_referral_code_by_user_id(db, user_id)
    if existing_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Referral code already exists'
        )

    referral_code = await create_referral_code(db, referral_code_create_schema, user_id)

    cache[user_id] = referral_code

    return ReferralCodeResponseSchema.from_orm(referral_code)


@router.delete(
    '/ref/delete',
    summary='Delete a referral code',
    description='This endpoint allows an authenticated user to delete their referral code. '
                'If no referral code exists for the user, a 404 error will be raised.'
)
async def delete_ref_code(
        db: Annotated[AsyncSession, Depends(get_db)],
        user_id: Annotated[int, Depends(get_user_id_from_token)],
):
    referral_code = await get_referral_code_by_user_id(db, user_id)
    if not referral_code:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Referral code not found'
        )

    await delete_referral_code(db, referral_code.id)

    if user_id in cache:
        del cache[user_id]


@router.get(
    '/ref/{email}',
    summary='Get referral code by email',
    description='This endpoint allows you to retrieve a referral code by providing the email address of the user. '
                'If no referral code is found for the given email, a 404 error will be raised.'
)
async def get_ref_code_by_email(
        db: Annotated[AsyncSession, Depends(get_db)],
        email: EmailStr,
) -> ReferralCodeResponseSchema:
    referral_code = await get_referral_code_by_email(db, email)
    if not referral_code:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Referral code not found'
        )
    return referral_code


@router.get(
    '/referrals/{referrer_id}',
    summary='Get referrals by referrer ID',
    description='This endpoint allows you to get a list of users who were referred by a specific referrer, '
                'identified by their referrer ID. If no referrals exist for the given referrer, an empty list'
                ' will be returned.'
)
async def get_referrals(
        db: Annotated[AsyncSession, Depends(get_db)],
        referrer_id: int,
) -> Sequence[UserResponseSchema]:
    referrals = await get_referrals_by_referrer_id(db, referrer_id)
    return referrals

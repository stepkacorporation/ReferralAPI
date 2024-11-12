from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.database.crud.user import get_user_by_email, create_user, get_user_by_id
from app.schemas import UserCreateSchema, TokenResponseSchema, UserResponseSchema
from app.services.auth import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_user_id_from_token,
)
from app.services.user import create_user_with_referral
from app.utils.security import verify_password

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post(
    '/signup',
    status_code=status.HTTP_201_CREATED,
    summary='Register a new user',
    description='This endpoint registers a new user by accepting email, password and other details. '
                'If successful, it returns an access token and a refresh token for authentication.'
)
async def register_user(
        db: Annotated[AsyncSession, Depends(get_db)],
        user_create_schema: UserCreateSchema,
) -> TokenResponseSchema:
    existing_user = await get_user_by_email(db, user_create_schema.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email is already registered'
        )

    user = await create_user_with_referral(db, user_create_schema)

    access_token = create_access_token({'sub': str(user.id)})
    refresh_token = create_refresh_token({'sub': str(user.id)})

    return TokenResponseSchema(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type='bearer'
    )


@router.post(
    '/login',
    summary='Log in a user',
    description='This endpoint allows users to authenticate by providing their email and password. '
                'Upon successful authentication, it returns an access token and a refresh token.'
)
async def login_user(
        db: Annotated[AsyncSession, Depends(get_db)],
        user_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> TokenResponseSchema:
    user = await get_user_by_email(db, user_data.username)
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Incorrect email or password'
        )

    access_token = create_access_token({'sub': str(user.id)})
    refresh_token = create_refresh_token({'sub': str(user.id)})

    return TokenResponseSchema(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type='bearer'
    )


@router.post(
    '/refresh',
    summary='Refresh access and refresh tokens',
    description='This endpoint allows users to refresh their access and refresh tokens using a valid refresh token. '
                'If the provided token is valid, new tokens are returned.'
)
async def refresh_user_token(token: str) -> TokenResponseSchema:
    payload = decode_token(token, settings.SECRET_KEY_REFRESH)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token',
            headers={'WWW-Authenticate': 'Bearer'}
        )

    id_: str = payload.get('sub')
    if id_ is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token',
            headers={'WWW-Authenticate': 'Bearer'}
        )

    access_token = create_access_token({'sub': str(id_)})
    refresh_token = create_refresh_token({'sub': str(id_)})

    return TokenResponseSchema(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type='bearer'
    )


@router.get(
    '/me',
    summary='Get current user information',
    description='This endpoint retrieves the current authenticated user\'s information using their access token. '
                'It returns the user\'s details.'
)
async def read_current_user(
        db: Annotated[AsyncSession, Depends(get_db)],
        user_id: Annotated[int, Depends(get_user_id_from_token)],
) -> UserResponseSchema:
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )

    return UserResponseSchema.from_orm(user)


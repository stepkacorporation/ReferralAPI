from typing import Annotated

from datetime import datetime, timezone, timedelta

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login', scheme_name='JWT')


def _create_token(
        data: dict,
        secret_key: str,
        expires_delta: timedelta,
) -> str:
    """
    Generates a JWT token.

    Args:
        - data (dict): The data to encode in the token.
        - secret_key (str): The secret key used to sign the token.
        - expires_delta (timedelta): The expiration time delta for the token.

    Returns:
        str: The encoded JWT token.

    Example:
        _create_token({"sub": "user123"}, "my_secret_key", timedelta(minutes=15))
    """

    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_access_token(
        data: dict,
        expires_delta: timedelta | None = None
) -> str:
    """
    Generates an access token (JWT) with a customizable expiration time.

    Args:
        - data (dict): The data to encode in the token.
        - expires_delta (timedelta, optional): The expiration time delta for the token.
                                             Defaults to a value defined in the settings if not provided.

    Returns:
        str: The generated access token (JWT).

    Example:
        create_access_token({"sub": "user123"})
        create_access_token({"sub": "user123"}, timedelta(hours=1))
    """

    return _create_token(
        data=data,
        secret_key=settings.SECRET_KEY_ACCESS,
        expires_delta=expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )


def create_refresh_token(
        data: dict,
        expires_delta: timedelta | None = None,
) -> str:
    """
    Generates a refresh token (JWT) with a customizable expiration time.

    Args:
        - data (dict): The data to encode in the token.
        - expires_delta (timedelta, optional): The expiration time delta for the token.
                                               Defaults to a value defined in the settings if not provided.

    Returns:
        str: The generated refresh token (JWT).

    Example:
        create_refresh_token({"sub": "user123"})
        create_refresh_token({"sub": "user123"}, timedelta(days=30))
    """

    return _create_token(
        data=data,
        secret_key=settings.SECRET_KEY_REFRESH,
        expires_delta=expires_delta or timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )


def decode_token(token: str, key: str) -> dict | None:
    """
    Decodes a JWT token and returns the payload.

    Args:
        - token (str): The JWT token to decode.
        - key (str): The secret key used to validate the token's signature.

    Returns:
        dict: The payload decoded from the token.

    Raises:
        - HTTPException: If the token is expired, raises a 403 Forbidden error.
        - HTTPException: If the token is invalid, raises a 401 Unauthorized error.

    Example:
        decode_token("your_jwt_token", "secret_key")
    """

    try:
        payload = jwt.decode(token, key, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Token expired',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    except jwt.JWTError as error:
        print(f'ОШИБКА В decode_token: {error}')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token',
            headers={'WWW-Authenticate': 'Bearer'}
        )


async def get_user_id_from_token(token: Annotated[str, Depends(oauth2_scheme)]) -> int:
    """
    Retrieve the current authenticated user's ID from the provided JWT token.

    Params:
        - token (str): The JWT token provided by the user.
        - db (AsyncSession): The database session.

    Returns:
        - int: The current user's ID.

    Raises:
        - HTTPException: If the token is invalid, expired, or cannot be decoded.
    """

    payload = decode_token(token, settings.SECRET_KEY_ACCESS)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate user',
            headers={'WWW-Authenticate': 'Bearer'}
        )

    user_id = payload.get('sub')
    expire = payload.get('exp')

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate user',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    if expire is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No access token supplied',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    if datetime.now(timezone.utc) > datetime.fromtimestamp(expire, tz=timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Token expired',
            headers={'WWW-Authenticate': 'Bearer'}
        )

    try:
        user_id = int(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate user',
            headers={'WWW-Authenticate': 'Bearer'}
        )

    return user_id

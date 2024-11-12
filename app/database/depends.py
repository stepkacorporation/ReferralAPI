from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides an asynchronous database session.

    Yields:
       -  AsyncSession: An asynchronous session to interact with the database.
    """

    async with AsyncSessionLocal() as session:
        yield session

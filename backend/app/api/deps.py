from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from redis import ConnectionPool, StrictRedis
from sqlmodel import Session

from app.core.config import settings
from app.core.database import engine

redis_pool = ConnectionPool(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True,
)


def get_redis_client() -> Generator[StrictRedis, None, None]:
    """Yields a Redis client from the global connection pool."""
    redis_client = StrictRedis(connection_pool=redis_pool)
    try:
        yield redis_client
    finally:
        # Redis connection pools handle cleanup automatically
        pass


RedisSessionDep = Annotated[StrictRedis, Depends(get_redis_client)]


def get_db() -> Generator[Session, None, None]:
    """Yields a database session."""
    with Session(engine) as session:
        yield session


DBSessionDep = Annotated[Session, Depends(get_db)]

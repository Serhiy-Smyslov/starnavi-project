import asyncio
from typing import Generator, Callable, AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.core.config import settings
from app.db.base import Base
from app.db.session import SessionLocal


@pytest.fixture(scope="session")
def event_loop(request) -> Generator:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def db_engine(request):
    """yields a SQLAlchemy engine which is suppressed after the test session"""
    db_url = settings.SQLALCHEMY_DATABASE_URI
    engine_ = create_async_engine(db_url, echo=settings.DB_ECHO_LOG)

    yield engine_

    await engine_.dispose()


@pytest.fixture()
async def db_session(db_engine) -> AsyncSession:
    async with db_engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
        async with SessionLocal(bind=connection) as session:
            yield session
            await session.flush()
            await session.rollback()


@pytest.fixture()
def override_get_db(db_session: AsyncSession) -> Callable:
    async def _override_get_db():
        yield db_session

    return _override_get_db


@pytest.fixture()
def app(override_get_db: Callable) -> FastAPI:
    from app.api.deps import get_db
    from app.main import app

    app.dependency_overrides[get_db] = override_get_db
    return app


@pytest.fixture()
async def async_client(app: FastAPI) -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="http://test/") as ac:
        yield ac

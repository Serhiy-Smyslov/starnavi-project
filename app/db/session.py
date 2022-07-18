from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, future=True, echo=settings.DB_ECHO_LOG)
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

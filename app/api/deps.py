from datetime import datetime
from typing import Optional

from fastapi import Depends, Request, Security
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.db.session import SessionLocal
from app.exceptions.api_exceptions import AccessDenied
from app.models import User
from app.schemas import UserLastRequest

authorization_token = APIKeyHeader(name='Authorization', auto_error=False)


async def get_db() -> AsyncSession:
    """
    Dependency function that yields db sessions
    """
    async with SessionLocal() as session:
        yield session
        await session.commit()


async def is_authorized(
        db: AsyncSession = Depends(get_db),
        *,
        request: Request,
        authorization: Optional[str] = Security(authorization_token)) -> User:
    if not authorization:
        authorization = request.headers.get('authorization', '')
    user = await crud.user.get_by_access_token(db=db, access_token=authorization)
    if not user:
        raise AccessDenied()
    last_login_in = UserLastRequest(last_request=datetime.utcnow())
    await crud.user.update(db=db, db_obj=user, obj_in=last_login_in)
    return user

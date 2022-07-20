from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app import models, crud
from app.auth.auth import AuthService
from app.schemas import UserCreate
from app.tests.utils.utils import random_lower_string, random_email


async def create_random_user(db: AsyncSession, **kwargs) -> models.User:
    password = AuthService.get_hashed_password(random_lower_string())
    access_token_expires = datetime.utcnow() + timedelta(seconds=3600)
    refresh_token_expires = datetime.utcnow() + timedelta(days=30)
    user_in = UserCreate(
        nickname=random_lower_string(),
        email=random_email(),
        password=password,
        access_token=random_lower_string(),
        refresh_token=random_lower_string(),
        access_token_expires=access_token_expires,
        refresh_token_expires=refresh_token_expires
    )

    for k, v in kwargs.items():
        setattr(user_in, k, v)

    return await crud.user.create(db=db, obj_in=user_in)

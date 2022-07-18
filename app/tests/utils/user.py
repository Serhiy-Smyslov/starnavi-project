from sqlalchemy.ext.asyncio import AsyncSession

from app import models, crud
from app.schemas import UserCreate
from app.tests.utils.utils import random_lower_string, random_email


async def create_random_user(db: AsyncSession, **kwargs) -> models.User:
    user_in = UserCreate(
        nickname=random_lower_string(),
        email=random_email(),
        password=random_lower_string()
    )

    for k, v in kwargs.items():
        setattr(user_in, k, v)

    return await crud.user.create(db=db, obj_in=user_in)

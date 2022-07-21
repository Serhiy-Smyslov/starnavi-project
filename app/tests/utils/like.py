from sqlalchemy.ext.asyncio import AsyncSession

from app import models, crud
from app.schemas import LikeCreate
from app.tests.utils.post import create_random_post
from app.tests.utils.user import create_random_user


async def create_random_like(db: AsyncSession, **kwargs) -> models.Like:
    user = await create_random_user(db=db)
    post = await create_random_post(db=db)
    like_in = LikeCreate(
        post_id=post.id,
        user_id=user.id
    )

    for k, v in kwargs.items():
        setattr(like_in, k, v)

    return await crud.like.create(db=db, obj_in=like_in)

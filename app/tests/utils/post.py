from sqlalchemy.ext.asyncio import AsyncSession

from app import models, crud
from app.schemas import PostCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


async def create_random_post(db: AsyncSession, **kwargs) -> models.Post:
    user = await create_random_user(db=db)
    post_in = PostCreate(
        title=random_lower_string(),
        text=random_lower_string(),
        creator_id=user.id
    )

    for k, v in kwargs.items():
        setattr(post_in, k, v)

    return await crud.post.create(db=db, obj_in=post_in)

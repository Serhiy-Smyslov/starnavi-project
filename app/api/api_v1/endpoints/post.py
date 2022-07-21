from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app import crud
from app.api import deps
from app.exceptions.api_exceptions import NotFound
from app.models import User
from app.schemas import PostCreate, Post, PostBase, LikeCreate

router = APIRouter()


@router.get('/', summary='Get post', response_model=Post)
async def get(*,
              db: AsyncSession = Depends(deps.get_db),
              user: User = Depends(deps.is_authorized),
              post_id: int) -> Post:
    post = await crud.post.get(db=db, id=post_id)
    if not post:
        raise NotFound(detail='Post not found')
    return post


@router.post('/', summary='Create new post', response_model=Post)
async def create(*,
                 db: AsyncSession = Depends(deps.get_db),
                 user: User = Depends(deps.is_authorized),
                 post_in: PostBase) -> Post:
    post_in = PostCreate(**post_in.dict(), creator_id=user.id)
    return await crud.post.create(db=db, obj_in=post_in)


@router.post('/like/', summary='User like/unlike post', status_code=status.HTTP_200_OK)
async def like_or_unlike(*,
                         db: AsyncSession = Depends(deps.get_db),
                         user: User = Depends(deps.is_authorized),
                         post_id: int) -> None:
    post = await crud.post.get(db=db, id=post_id)
    if not post:
        raise NotFound(detail='Post not found')
    user_like = await crud.like.get_user_like(db=db, post_id=post.id, user_id=user.id)
    if user_like:
        await crud.like.remove(db=db, obj=user_like)
    else:
        user_like_in = LikeCreate(user_id=user.id, post_id=post_id)
        await crud.like.create(db=db, obj_in=user_like_in)

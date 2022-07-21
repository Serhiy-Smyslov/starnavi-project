from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.config import settings
from app.schemas import PostBase
from app.tests.utils.post import create_random_post
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_int


class TestPost:
    async def test_get(self, async_client: AsyncClient, db_session: AsyncSession):
        user = await create_random_user(db_session)
        post = await create_random_post(db_session)

        headers = {'authorization': user.access_token}
        params = {'post_id': post.id}

        response = await async_client.get(f"{settings.API_V1_STR}/post/",
                                          params=params)
        assert response.status_code == 403

        fake_params = {'post_id': random_int()}

        response = await async_client.get(f"{settings.API_V1_STR}/post/",
                                          params=fake_params,
                                          headers=headers)
        assert response.status_code == 404

        response = await async_client.get(f"{settings.API_V1_STR}/post/",
                                          params=params,
                                          headers=headers)
        assert response.status_code == 200

        response = response.json()
        assert response['id'] == post.id
        assert response['title'] == post.title
        assert response['text'] == post.text

    async def test_create(self, async_client: AsyncClient, db_session: AsyncSession):
        user = await create_random_user(db_session)
        posts = await crud.post.get_multi(db=db_session)
        assert len(posts) == 0

        headers = {'authorization': user.access_token}
        post_in = PostBase(title="test",
                           text="test")

        response = await async_client.post(f"{settings.API_V1_STR}/post/",
                                           json=post_in.dict())
        assert response.status_code == 403

        response = await async_client.post(f"{settings.API_V1_STR}/post/",
                                           json=post_in.dict(),
                                           headers=headers)
        assert response.status_code == 200

        posts = await crud.user.get_multi(db=db_session)
        assert len(posts) == 1

    async def test_like_or_unlike(self, async_client: AsyncClient, db_session: AsyncSession):
        user = await create_random_user(db_session)
        post = await create_random_post(db_session)

        likes = await crud.like.get_multi(db=db_session)
        assert len(likes) == 0

        headers = {'authorization': user.access_token}
        params = {'post_id': post.id}

        response = await async_client.post(f"{settings.API_V1_STR}/post/like/",
                                           params=params)
        assert response.status_code == 403

        fake_params = {'post_id': random_int()}

        response = await async_client.post(f"{settings.API_V1_STR}/post/like/",
                                           params=fake_params,
                                           headers=headers)
        assert response.status_code == 404

        response = await async_client.post(f"{settings.API_V1_STR}/post/like/",
                                           params=params,
                                           headers=headers)
        assert response.status_code == 200

        likes = await crud.like.get_multi(db=db_session)
        assert len(likes) == 1

        response = await async_client.post(f"{settings.API_V1_STR}/post/like/",
                                           params=params,
                                           headers=headers)
        assert response.status_code == 200

        likes = await crud.like.get_multi(db=db_session)
        assert len(likes) == 0

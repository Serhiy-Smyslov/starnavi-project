import asyncio
from datetime import timedelta, date

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.config import settings
from app.tests.utils.like import create_random_like


class TestAnalyst:
    async def test_count_likes(self, async_client: AsyncClient, db_session: AsyncSession):
        like = await create_random_like(db_session)

        likes = await crud.like.get_multi(db=db_session)
        assert len(likes) == 1

        date_from = date.today() - timedelta(days=2)
        params = {'date_from': date_from,
                  'date_to': date.today()}

        response = await async_client.get(f"{settings.API_V1_STR}/analyst/likes-for-day/",
                                          params=params)
        assert response.status_code == 200
        response = response.json()

        assert response['post_amount_likes'] == 1

        date_from = date.today() - timedelta(days=10)
        date_to = date.today() - timedelta(days=3)
        params = {'date_from': date_from,
                  'date_to': date_to}

        response = await async_client.get(f"{settings.API_V1_STR}/analyst/likes-for-day/",
                                          params=params)
        assert response.status_code == 200
        response = response.json()

        assert response['post_amount_likes'] == 0


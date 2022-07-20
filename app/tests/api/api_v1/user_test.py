from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.auth.auth import AuthService
from app.core.config import settings
from app.schemas import UserCreate, UserLogin
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


class TestUser:
    async def test_sign_up(self, async_client: AsyncClient, db_session: AsyncSession):
        users = await crud.user.get_multi(db=db_session)
        assert len(users) == 0

        user_in = UserCreate(email="test@test.com",
                             password="test")

        response = await async_client.post(f"{settings.API_V1_STR}/auth/sign-up/",
                                           json=user_in.dict())
        assert response.status_code == 200

        users = await crud.user.get_multi(db=db_session)
        assert len(users) == 1

    async def test_login(self, async_client: AsyncClient, db_session: AsyncSession):
        password = 'test'
        hash_password = AuthService.get_hashed_password(password)
        user = await create_random_user(db=db_session, password=hash_password)

        user_in = UserLogin(email=user.email, password=password)
        response = await async_client.post(f"{settings.API_V1_STR}/auth/login/",
                                           json=user_in.dict())

        assert response.status_code == 200
        assert user.access_token
        assert user.refresh_token
        assert user.access_token_expires
        assert user.refresh_token_expires

    async def test_logout(self, async_client: AsyncClient, db_session: AsyncSession):
        user = await create_random_user(db_session)
        headers = {'authorization': user.access_token}

        response = await async_client.post(f"{settings.API_V1_STR}/auth/logout/",
                                           headers=headers)
        assert response.status_code == 200
        assert user.access_token is None
        assert user.refresh_token is None
        assert user.access_token_expires is None
        assert user.refresh_token_expires is None

    async def test_refresh_access_token(self, async_client: AsyncClient, db_session: AsyncSession):
        user = await create_random_user(db_session)
        old_token = user.access_token

        params = {'refresh_token': user.refresh_token}
        response = await async_client.post(f"{settings.API_V1_STR}/auth/refresh-token/",
                                           params=params)

        assert response.status_code == 200
        response = response.json()
        assert response['access_token'] != old_token

        params = {'refresh_token': random_lower_string()}
        response = await async_client.post(f"{settings.API_V1_STR}/auth/refresh-token/",
                                           params=params)

        assert response.status_code == 403


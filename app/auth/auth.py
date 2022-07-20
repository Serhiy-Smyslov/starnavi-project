import logging
from datetime import datetime, timedelta
from typing import Optional

import jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.config import settings
from app.exceptions.api_exceptions import RefreshDenied
from app.schemas import User, UserTokens, UserAccessToken


class AuthService:
    PASSWORD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def get_hashed_password(password: str) -> str:
        return AuthService.PASSWORD_CONTEXT.hash(password)

    @staticmethod
    def verify_password(password: str, hashed_pass: str) -> bool:
        return AuthService.PASSWORD_CONTEXT.verify(password, hashed_pass)

    @staticmethod
    def create_access_token(subjects: dict, expires_delta: Optional[int] = None) -> dict:
        if expires_delta is not None:
            expires_date = datetime.utcnow() + timedelta(minutes=expires_delta)
        else:
            expires_date = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        subjects['expires_date'] = expires_date.isoformat()
        encoded_jwt = jwt.encode(subjects, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)

        access_token_data = {'access_token': encoded_jwt, 'access_token_expires': expires_date}
        return access_token_data

    @staticmethod
    def create_refresh_token(subjects: dict, expires_delta: Optional[int] = None) -> dict:
        if expires_delta is not None:
            expires_date = datetime.utcnow() + timedelta(minutes=expires_delta)
        else:
            expires_date = datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

        subjects['refresh_token_expires'] = expires_date.isoformat()
        encoded_jwt = jwt.encode(subjects, settings.JWT_REFRESH_SECRET_KEY, settings.JWT_ALGORITHM)

        refresh_token_data = {'refresh_token': encoded_jwt, 'refresh_token_expires': expires_date}
        return refresh_token_data

    @staticmethod
    async def update_user_tokens(db: AsyncSession, user: User) -> UserTokens:
        subjects = {
            'email': user.email,
            'nickname': user.nickname
        }
        access_token = AuthService.create_access_token(subjects=subjects)
        refresh_token = AuthService.create_refresh_token(subjects=subjects)

        user_tokens = UserTokens(**access_token, **refresh_token)
        await crud.user.update(db=db, db_obj=user, obj_in=user_tokens)
        return user_tokens

    @staticmethod
    async def refresh_access_token(db: AsyncSession, refresh_token: str) -> UserAccessToken:
        user = await crud.user.get_by_refresh_token(db=db, refresh_token=refresh_token)
        if not user:
            logging.error(f'User not found by refresh_token={refresh_token}')
            raise RefreshDenied(detail='Invalid refresh token')

        subjects = {
            'email': user.email,
            'nickname': user.nickname
        }
        access_token_data = AuthService.create_access_token(subjects=subjects)
        user_in = UserAccessToken(**access_token_data)
        await crud.user.update(db=db, db_obj=user, obj_in=user_in)
        return user_in

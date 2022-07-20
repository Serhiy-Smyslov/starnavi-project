from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app import crud
from app.api import deps
from app.auth.auth import AuthService
from app.exceptions.api_exceptions import UserExist, NotFound, IncorrectData
from app.models import User
from app.schemas import UserTokens, UserLogin, UserAccessToken, UserAuth

router = APIRouter()


@router.post('/sign-up/', summary='Create new user', response_model=UserTokens)
async def sing_up(*, db: AsyncSession = Depends(deps.get_db), user_in: UserAuth) -> UserTokens:
    user = await crud.user.get_by_email(db=db, email=user_in.email)
    if user:
        raise UserExist(detail='User with this email already exist')
    user_in.password = AuthService.get_hashed_password(user_in.password)
    user = await crud.user.create(db=db, obj_in=user_in)
    tokens = await AuthService.update_user_tokens(db=db, user=user)
    return tokens


@router.post('/login/', summary='Login user in the system', response_model=UserTokens)
async def login(*, db: AsyncSession = Depends(deps.get_db), user_in: UserLogin) -> UserTokens:
    user = await crud.user.get_by_email(db=db, email=user_in.email)
    if not user:
        raise NotFound(detail='The user is not register')
    if not AuthService.verify_password(user_in.password, user.password):
        raise IncorrectData(detail='Incorrect password')
    tokens = await AuthService.update_user_tokens(db=db, user=user)
    return tokens


@router.post('/logout/', summary='Logout user from the system', status_code=status.HTTP_200_OK)
async def logout(*,
                 db: AsyncSession = Depends(deps.get_db),
                 user: User = Depends(deps.is_authorized)) -> None:
    user_in = UserTokens(access_token=None,
                         refresh_token=None,
                         access_token_expires=None,
                         refresh_token_expires=None)
    await crud.user.update(db=db, db_obj=user, obj_in=user_in)


@router.post('/refresh-token/', summary='Refresh user access token', response_model=UserAccessToken)
async def refresh_access_token(*,
                               db: AsyncSession = Depends(deps.get_db),
                               refresh_token: str) -> UserAccessToken:
    return await AuthService.refresh_access_token(db=db, refresh_token=refresh_token)

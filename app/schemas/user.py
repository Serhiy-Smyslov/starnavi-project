from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    nickname: Optional[str] = None
    email: str
    password: str
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    access_token_expires: Optional[datetime] = None
    refresh_token_expires: Optional[datetime] = None


class UserUpdate(UserBase):
    pass


class UserCreate(UserBase):
    pass


class UserAuth(BaseModel):
    nickname: Optional[str] = None
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserTokens(BaseModel):
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    access_token_expires: Optional[datetime] = None
    refresh_token_expires: Optional[datetime] = None


class UserAccessToken(BaseModel):
    access_token: str
    access_token_expires: datetime


class UserInDBBase(UserBase):
    id: int

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass

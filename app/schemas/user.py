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


class UserLastLogin(BaseModel):
    last_login: datetime


class UserLastRequest(BaseModel):
    last_request: datetime


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
    last_login: Optional[datetime] = None
    last_request: Optional[datetime] = None

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass


class UserProfile(BaseModel):
    id: int
    nickname: Optional[str] = None
    email: str
    last_login: Optional[datetime] = None
    last_request: Optional[datetime] = None

    class Config:
        orm_mode = True

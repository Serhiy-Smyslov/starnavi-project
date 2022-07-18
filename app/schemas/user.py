from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    nickname: Optional[str] = None
    email: str
    password: str


class UserUpdate(UserBase):
    pass


class UserCreate(UserBase):
    pass


class UserInDBBase(UserBase):
    id: int

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass

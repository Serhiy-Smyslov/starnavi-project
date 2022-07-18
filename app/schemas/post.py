from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas import User


class PostBase(BaseModel):
    title: str
    text: Optional[str] = None
    creator_id: int


class PostUpdate(PostBase):
    pass


class PostCreate(PostBase):
    pass


class PostInDBBase(PostBase):
    id: int
    creator: User
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class Post(PostInDBBase):
    pass

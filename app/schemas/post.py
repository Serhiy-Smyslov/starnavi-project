from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from app.schemas import UserProfile
from app.schemas.like import Like


class PostBase(BaseModel):
    title: str
    text: Optional[str] = None


class PostUpdate(PostBase):
    pass


class PostCreate(PostBase):
    creator_id: int


class PostInDBBase(PostBase):
    id: int
    creator: UserProfile
    likes: List[Optional[Like]]
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class Post(PostInDBBase):
    pass

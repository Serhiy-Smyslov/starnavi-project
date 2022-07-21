from datetime import datetime

from pydantic import BaseModel


class LikeBase(BaseModel):
    user_id: int
    post_id: int


class LikeUpdate(LikeBase):
    pass


class LikeCreate(LikeBase):
    pass


class LikeStatistic(BaseModel):
    post_amount_likes: int


class LikeInDBBase(LikeBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class Like(LikeInDBBase):
    pass

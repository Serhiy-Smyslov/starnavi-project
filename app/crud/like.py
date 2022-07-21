from datetime import date
from typing import Any

from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Like
from app.schemas import LikeCreate, LikeUpdate


class CRUDLike(CRUDBase[Like, LikeCreate, LikeUpdate]):
    async def get_user_like(self, db: AsyncSession, post_id: int, user_id: int) -> Any:
        q = select(self.model).where(and_(self.model.post_id == post_id, self.model.user_id == user_id))
        query = await db.execute(q)
        return query.scalar()

    async def count_likes(self,
                          db: AsyncSession,
                          date_from: date,
                          date_to: date) -> Any:
        query = select(func.count(self.model.id).label('post_amount_likes')).filter(and_(
            func.date(self.model.created_at) >= date_from, func.date(self.model.created_at) <= date_to))
        q = await db.execute(query)
        return q.fetchone()


like = CRUDLike(Like)

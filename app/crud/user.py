from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import User
from app.schemas import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        q = select(self.model).where(self.model.email == email)
        query = await db.execute(q)
        return query.scalar()

    async def get_by_access_token(self,
                                  db: AsyncSession,
                                  access_token: str):
        current_time = datetime.utcnow()
        query = select(self.model).where(self.model.access_token == access_token).filter(
            self.model.access_token_expires >= current_time)
        q = await db.execute(query)
        return q.scalar()

    async def get_by_refresh_token(self,
                                   db: AsyncSession,
                                   *,
                                   refresh_token: str):
        current_time = datetime.utcnow()
        query = select(self.model).where(self.model.refresh_token == refresh_token).filter(
            self.model.refresh_token_expires >= current_time)
        q = await db.execute(query)
        return q.scalar()


user = CRUDUser(User)

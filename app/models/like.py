from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, UniqueConstraint

from app.db.base_class import Base


class Like(Base):
    __table_args__ = (UniqueConstraint('user_id', 'post_id'),)
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(ForeignKey('user.id'), primary_key=True)
    post_id = Column(ForeignKey('post.id'), primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

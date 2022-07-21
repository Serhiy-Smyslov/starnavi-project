from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Post(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    text = Column(String, nullable=False)
    creator_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    creator = relationship('User', lazy='immediate')
    likes = relationship('Like', lazy='immediate')

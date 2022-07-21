from sqlalchemy import Column, Integer, String, DateTime

from app.db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    nickname = Column(String, index=True, nullable=True)
    password = Column(String, nullable=False)

    access_token = Column(String, unique=True, nullable=True)
    refresh_token = Column(String, unique=True, nullable=True)
    access_token_expires = Column(DateTime(timezone=True), nullable=True)
    refresh_token_expires = Column(DateTime(timezone=True), nullable=True)

    last_login = Column(DateTime(timezone=True), nullable=True)
    last_request = Column(DateTime(timezone=True), nullable=True)

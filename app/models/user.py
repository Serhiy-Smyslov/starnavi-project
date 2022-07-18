from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    nickname = Column(String, index=True, nullable=True)
    password = Column(String, nullable=False)

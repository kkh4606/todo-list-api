from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"))


class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, nullable=False)
    content = Column(String, nullable=False)
    is_completed = Column(Boolean, server_default="FALSE")
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"))

    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    owner = relationship("User")

from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import declarative_base, relationship
from app.db.db import Base


class Thread(Base):
    __tablename__ = 'thread'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(20), nullable=False)
    title = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    created_timestamp = Column(DateTime(timezone=True), server_default=func.now())
    modified_timestamp = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    user = relationship('User', back_populates='threads')
    messages = relationship('ThreadMessage', back_populates='thread', cascade="all, delete-orphan")

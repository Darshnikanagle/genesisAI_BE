from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import declarative_base, relationship
from app.db.db import Base

class ThreadMessage(Base):
    __tablename__ = 'thread_message'

    id = Column(Integer, primary_key=True, autoincrement=True)
    thread_id = Column(Integer, ForeignKey('thread.id', ondelete="CASCADE"), nullable=False)
    user_type = Column(Text, nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    thread = relationship('Thread', back_populates='messages')

from sqlalchemy import Column, Integer, String
from app.db.db import Base
from sqlalchemy.orm import declarative_base, relationship

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    password = Column(String(50))

    threads = relationship('Thread', back_populates='user')

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"


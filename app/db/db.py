from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.constants import GENESIS_DATABASE_DIRECTORY

DATABASE_URL = "sqlite:///" + GENESIS_DATABASE_DIRECTORY

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
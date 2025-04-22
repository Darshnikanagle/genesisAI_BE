from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from models.thread_model  import User
from constants import GENESIS_DATABASE_DIRECTORY

engine = create_engine("sqlite:///" + GENESIS_DATABASE_DIRECTORY, echo=True)

Session = sessionmaker(bind=engine)
session = Session()

# Add new user
new_user = User(name="Alice", email="kbvarma@gmail.com", password="Admin")
session.add(new_user)
session.commit()

# Query
for user in session.query(User).all():
    print(user.id, user.name)

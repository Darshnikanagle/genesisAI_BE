


from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.models.user_model import User
from passlib.context import CryptContext
from pydantic import BaseModel
from app.crud.user_crud import get_user_by_email, create_user

from app.db.db import SessionLocal

# session = Session()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Request body schemas
class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

# Utils
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Add new user
@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(email = user.email, session = db)
    # existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password)
    )

    create_user(session = db, user = new_user)
    return {"message": "User registered successfully", "user_id": new_user.id}

# Login user
@router.post("/login")
def login_user(credentials: UserLogin, db: Session = Depends(get_db)):
    user = get_user_by_email(session=db, email = credentials.email)
    print("user found:", user)
    # user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {"message": "Login successful", "user_id": user.id}

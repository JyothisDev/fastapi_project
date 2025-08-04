# from fastapi import FastAPI
# from app.database import database, engine, metadata
# from app.routes import auth, messages
# from fastapi.middleware.cors import CORSMiddleware

# # Create tables on startup
# metadata.create_all(engine)

# app = FastAPI()

# # Allow all origins (e.g. Flutter frontend)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.on_event("startup")
# async def startup():
#     await database.connect()

# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()

# # Register routes
# app.include_router(auth.router, tags=["auth"])
# app.include_router(messages.router, tags=["messages"])
# FastAPI Backend (main.py)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SQLALCHEMY_DATABASE_URL = "sqlite:///./users.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

Base.metadata.create_all(bind=engine)

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class LoginModel(BaseModel):
    email: str
    password: str

class UserUpdate(BaseModel):
    username: str = None
    email: str = None
    password: str = None

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    class Config:
        orm_mode = True

@app.post("/register", response_model=UserOut)
def register(user: UserCreate):
    db = SessionLocal()
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    db_user = User(username=user.username, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/login", response_model=UserOut)
def login(user: LoginModel):
    db = SessionLocal()
    db_user = db.query(User).filter(User.email == user.email, User.password == user.password).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return db_user

@app.get("/user/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    db = SessionLocal()
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/user/{user_id}", response_model=UserOut)
def update_user(user_id: int, update: UserUpdate):
    db = SessionLocal()
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if update.username is not None:
        user.username = update.username
    if update.email is not None:
        user.email = update.email
    if update.password is not None:
        user.password = update.password
    db.commit()
    db.refresh(user)
    return user

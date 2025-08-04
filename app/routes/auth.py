from fastapi import APIRouter, HTTPException
from app.schemas import UserCreate, UserLogin, Token
from app.auth import hash_password, verify_password, create_access_token
from app.crud import create_user, get_user_by_username

router = APIRouter()

@router.post("/register", response_model=Token)
async def register(user: UserCreate):
    existing = await get_user_by_username(user.username)
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    
    hashed = hash_password(user.password)
    new_user = await create_user(user.username, hashed)
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    db_user = await get_user_by_username(user.username)
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

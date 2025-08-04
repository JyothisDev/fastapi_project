from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

# Secret key and algorithm
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash password
def hash_password(password: str):
    return pwd_context.hash(password)

# Verify password
def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

# Create JWT token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

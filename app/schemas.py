from pydantic import BaseModel

# For user registration/login
class UserCreate(BaseModel):
    username: str
    password: str

# For returning user info (no password)
class UserOut(BaseModel):
    id: int
    username: str

# Login request model
class UserLogin(BaseModel):
    username: str
    password: str

# JWT Token schema
class Token(BaseModel):
    access_token: str
    token_type: str

# Message input/output
class MessageIn(BaseModel):
    content: str

class MessageOut(BaseModel):
    id: int
    content: str

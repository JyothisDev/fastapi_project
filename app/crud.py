from app.models import users, messages
from app.database import database
from sqlalchemy import select

# Create a new user
async def create_user(username: str, password: str):
    query = users.insert().values(username=username, password=password)
    user_id = await database.execute(query)
    return {"id": user_id, "username": username}

# Get user by username
async def get_user_by_username(username: str):
    query = select(users).where(users.c.username == username)
    return await database.fetch_one(query)

# Save message
async def save_message(content: str):
    query = messages.insert().values(content=content)
    message_id = await database.execute(query)
    return {"id": message_id, "content": content}

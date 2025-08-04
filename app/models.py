from sqlalchemy import Table, Column, Integer, String
from app.database import metadata

# User table for login/register
users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, unique=True, nullable=False),
    Column("password", String, nullable=False),  # Stored as hashed password
)

# Message table
messages = Table(
    "messages",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("content", String),
)

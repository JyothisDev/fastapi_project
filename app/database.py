from databases import Database
from sqlalchemy import create_engine, MetaData

# Set the database URL (SQLite for simplicity)
DATABASE_URL = "sqlite:///./test.db"

# Async DB connection
database = Database(DATABASE_URL)

# SQLAlchemy metadata holds tables
metadata = MetaData()

# Sync engine (required by SQLAlchemy to create tables)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


# Import FastAPI framework
from fastapi import FastAPI

# Import BaseModel from Pydantic to define request schemas (data validation)
from pydantic import BaseModel

# Import Database class from `databases` to handle async DB operations
from databases import Database

# Import SQLAlchemy components to define the schema and create tables
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

# ✅ Add CORS middleware for allowing cross-origin requests (e.g., from Flutter web)
from fastapi.middleware.cors import CORSMiddleware

# --- DATABASE SETUP ---

# Define the database URL (using SQLite here)
DATABASE_URL = "sqlite:///./test.db"

# Create a database instance (asynchronous)
database = Database(DATABASE_URL)

# Create a metadata instance to hold table definitions
metadata = MetaData()

# Define the 'messages' table with columns: id and content
messages = Table(
    "messages",
    metadata,
    Column("id", Integer, primary_key=True),  # Auto-increment primary key
    Column("content", String),               # Content of the message
)

# Create a database engine for SQLite (with config to avoid thread issues)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create all tables defined in metadata if they don’t exist already
metadata.create_all(engine)

# --- FASTAPI APP SETUP ---

# Initialize the FastAPI app
app = FastAPI()

# ✅ Add CORS middleware to allow requests from any origin (especially for Flutter web)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 👈 Allow requests from all domains (e.g., localhost, web)
    allow_credentials=True,
    allow_methods=["*"],  # 👈 Allow all HTTP methods: GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # 👈 Allow all headers (e.g., Authorization, Content-Type)
)

# --- SCHEMA FOR REQUEST DATA ---

# Define the data model for POST request (e.g., {"content": "Hello"})
class MessageIn(BaseModel):
    content: str  # Accepts a string field named 'content'

# --- DATABASE CONNECTION EVENTS ---

# When the app starts up, connect to the database
@app.on_event("startup")
async def startup():
    await database.connect()

# When the app shuts down, disconnect from the database
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# --- API ENDPOINT ---

# Define a POST API endpoint at "/messages/" to create a new message
@app.post("/messages/")
async def create_message(msg: MessageIn):
    # Insert the new message content into the 'messages' table
    query = messages.insert().values(content=msg.content)
    
    # Execute the insert and get the new message's ID
    message_id = await database.execute(query)
    
    # Return the inserted data as JSON
    return {"id": message_id, "content": msg.content}

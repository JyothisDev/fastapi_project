from fastapi import FastAPI
from pydantic import BaseModel
from databases import Database
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from fastapi.middleware.cors import CORSMiddleware  # ✅ Add this

DATABASE_URL = "sqlite:///./test.db"

database = Database(DATABASE_URL)
metadata = MetaData()

messages = Table(
    "messages",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("content", String),
)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)

app = FastAPI()

# ✅ Add CORS middleware to allow requests from Flutter web or any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 👈 Allow all origins; for production, use specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessageIn(BaseModel):
    content: str

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/messages/")
async def create_message(msg: MessageIn):
    query = messages.insert().values(content=msg.content)
    message_id = await database.execute(query)
    return {"id": message_id, "content": msg.content}

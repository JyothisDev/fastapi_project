from fastapi import APIRouter
from app.schemas import MessageIn, MessageOut
from app.crud import save_message

router = APIRouter()

@router.post("/messages", response_model=MessageOut)
async def post_message(msg: MessageIn):
    return await save_message(msg.content)

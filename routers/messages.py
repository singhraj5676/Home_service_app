# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from database import get_db
# from schemas.auth_models import MessageCreate
# from models.user_models import UserInDB
# from models.chats import Chat
# from models.messages import Message
# from models.chat_participant import ChatParticipant
# from auth import get_current_user
# import datetime
# router = APIRouter()


# @router.post("/messages/", response_model=int)
# def create_message(message_create: MessageCreate, db: Session = Depends(get_db)):
#     # Validate that the chat exists
#     chat = db.query(Chat).filter(Chat.id == message_create.chat_id).first()
#     if not chat:
#         raise HTTPException(status_code=404, detail="Chat not found")

#     # Validate that the sender exists
#     sender = db.query(UserInDB).filter(UserInDB.id == message_create.sender_id).first()
#     if not sender:
#         raise HTTPException(status_code=404, detail="Sender not found")

#     # Create the new message
#     new_message = Message(
#         chat_id=message_create.chat_id,
#         sender_id=message_create.sender_id,
#         text=message_create.text,
#         created_at=datetime.datetime.utcnow()
#     )
#     db.add(new_message)
#     db.commit()
#     db.refresh(new_message)

#     return new_message.id
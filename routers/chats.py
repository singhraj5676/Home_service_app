# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from database import get_db
# from schemas.auth_models import ChatCreate
# from models.user_models import UserInDB
# from models.chats import Chat
# from models.chat_participant import ChatParticipant
# from auth import get_current_user
# import datetime
# router = APIRouter()


# @router.post("/chats/", response_model=int)
# def create_chat(chat_create: ChatCreate, db:Session = Depends(get_db)):
#     customer = db.query(UserInDB).filter(UserInDB.id == chat_create.customer_id).first()
#     worker = db.query(UserInDB).filter(UserInDB.id == chat_create.worker_id).first()
#     if not customer or not worker:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     new_chat = Chat(
#         id = int, 
#         create_at = datetime.datetime.utcnow(),
#         update_at = datetime.datetime.utcnow(),
#         is_group = chat_create.is_group
#     )
#     db.add(new_chat)
#     db.commit()

#     chat_participants = [
#         ChatParticipant(user_id=chat_create.customer_id, chat_id=new_chat.id),
#         ChatParticipant(user_id=chat_create.worker_id, chat_id=new_chat.id)
#     ]
#     db.add_all(chat_participants)
#     db.commit()

#     return new_chat.id
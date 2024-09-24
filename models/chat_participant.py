import datetime
from models.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer,  ForeignKey, DateTime


class ChatParticipant(Base):
    __tablename__ = 'chat_participants'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    chat_id = Column(Integer, ForeignKey('chats.id'), nullable=False)
    joined_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("UserInDB", back_populates="chats")
    chat = relationship("Chat", back_populates="participants")



#messages.py
import datetime
from models.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer,  ForeignKey
from sqlalchemy import Column, ForeignKey, Text, DateTime


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    chat_id = Column(Integer, ForeignKey('chats.id'), nullable=False)
    sender_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)

    # Relationships to chat and sender (user)
    chat = relationship("Chat", back_populates="messages")
    sender = relationship("UserInDB", back_populates="sent_messages")
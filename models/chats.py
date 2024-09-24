import datetime
from models.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, DateTime, Boolean



class Chat(Base):
    __tablename__ = 'chats'
    print('create chat table')

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.datetime.utcnow)
    is_group = Column(Boolean, default=False)

      # Relationships
    messages = relationship("Message", back_populates="chat")
    participants = relationship("ChatParticipant", back_populates="chat")
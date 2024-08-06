# models/verification_models.py
from models.base import Base
from models.user_models import UserInDB
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer


class VerificationToken(Base):
    __tablename__ = 'verification_tokens'

    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String, nullable=False, unique=True)
    expiration = Column(DateTime, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey(UserInDB.id), nullable=False)
    type = Column(String, nullable=False) 
    

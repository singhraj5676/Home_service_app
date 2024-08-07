#models/user_models.py
import uuid
from models.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Boolean, Float , Integer, DateTime




class UserInDB(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String, nullable=True)  # Allow first_name to be nullable
    last_name = Column(String, nullable=True)  # Allow last_name to be nullable
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    disabled = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    is_online = Column(Boolean, default=False)
    is_suspended = Column(Boolean, default=False)
    score = Column(Float, nullable=True)
    votes = Column(Integer, nullable=True)
    phone_number = Column(String, nullable=True)
    domain = Column(String, nullable=True)
    domain_language = Column(String, nullable=True)
    last_login = Column(DateTime, nullable=True)
    disabled = Column(Boolean, default=False)
   

    location = relationship("Location", back_populates="user", uselist=False)
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    verification_tokens = relationship("VerificationToken", back_populates="user")
    verification_types = relationship("VerificationType", back_populates="user")

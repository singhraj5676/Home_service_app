#models/user_models.py
import uuid
from models.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Boolean, Float , Integer, DateTime


from models.add_blockers import AddBlockers
from models.available_day import AvailableDay

class UserInDB(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
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

    location = relationship("Location", back_populates="user", uselist=False)
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    verification_tokens = relationship("VerificationToken", back_populates="user")
    verification_types = relationship("VerificationType", back_populates="user")
    languages = relationship("Language", back_populates="user")
    currency = relationship("Currency", back_populates="user")
    add_blockers = relationship("AddBlockers", back_populates="user")  # Relationship to AddBlockers
    available_days = relationship("AvailableDay", back_populates="user")
    given_reviews = relationship("Review", foreign_keys="Review.author_id", back_populates="author")
    received_reviews = relationship("Review", foreign_keys="Review.receiver_id", back_populates="receiver")
    adds_to_favorite = relationship("Favourite", foreign_keys="[Favourite.favors_id]", back_populates="favors")
    added_by_favorites = relationship("Favourite", foreign_keys="[Favourite.favored_by_id]", back_populates="favored_by")
    # blockers = relationship("Blockers", back_populates="user")





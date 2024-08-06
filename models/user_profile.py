#models/user_profile.py
import time
from models.base import Base
from models.user_models import UserInDB
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey



class UserProfile(Base):
    __tablename__ = 'user_profiles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    max_distance = Column(Integer, default=0)
    currency = Column(String, default="")
    amount = Column(Integer, default=0)
    experience = Column(Integer, default=0)
    personal_note = Column(String, default="")
    published = Column(Boolean, default=False)
    user_alert = Column(Boolean, default=True)
    personal_message = Column(Boolean, default=True)
    duration = Column(Integer,default=0),
    registered_date = Column(Integer, default=int(time.time()))
    user_id = Column(UUID(as_uuid=True), ForeignKey(UserInDB.id), nullable=False)



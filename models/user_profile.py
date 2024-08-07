#models/user_profile.py
import time
import enum
from sqlalchemy import Enum
from models.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey



class RoleEnum(enum.Enum):
    worker = "worker"
    customer = "customer"


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
    role = Column(Enum(RoleEnum), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'),nullable=False)

    user = relationship("UserInDB", back_populates="profile")





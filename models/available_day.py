#available_day.py
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from models.base import Base
from models.day import Days

class AvailableDay(Base):
    __tablename__ = 'available_days'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    day_id = Column(Integer, ForeignKey('days.id'), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)

    day = relationship("Days", back_populates="available_days")
    user = relationship("UserInDB", back_populates="available_days")

    def __repr__(self):
        return f"<AvailableDay(id={self.id}, day_id={self.day_id}, user_id={self.user_id})>"

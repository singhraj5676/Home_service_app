#day.py
from models.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String

class Days(Base):
    __tablename__ = 'days'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)  # e.g., "Monday", "Tuesday"

    available_days = relationship("AvailableDay", back_populates="day")
    
    def __repr__(self):
        return f"<Day(id={self.id}, name={self.name})>"

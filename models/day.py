#day.py
from models.base import Base
from sqlalchemy import Column, Integer, String

class Day(Base):
    __tablename__ = 'days'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)  # e.g., "Monday", "Tuesday"
    
    def __repr__(self):
        return f"<Day(id={self.id}, name={self.name})>"

#models/location.py

from models.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Float, Integer, ForeignKey


class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    city = Column(String, nullable=False)
    slug = Column(String, nullable=True)
    country = Column(String, nullable=False)
    country_code = Column(String, nullable=False)
    place_id = Column(String, nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)


    user = relationship("UserInDB", back_populates="location")

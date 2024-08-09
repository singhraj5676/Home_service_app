from models.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String, ForeignKey



class Currency(Base):
    __tablename__ = 'currencies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String, nullable=False, unique=True)  # ISO 4217 currency code, e.g., USD
    name = Column(String, nullable=False)  # Full name of the currency, e.g., US Dollar
    symbol = Column(String, nullable=True)  
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)

    user = relationship("UserInDB", back_populates="currency")
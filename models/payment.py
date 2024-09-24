import uuid
from models.base import Base
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import datetime
from sqlalchemy.orm import relationship
  # Import your base model

class Payment(Base):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    place_id = Column(String, nullable=False)
    redirect_url = Column(String, nullable=False)
    currency = Column(String(3), nullable=False)  # ISO currency code, e.g., EUR, USD
    locale = Column(String(5), nullable=False)  # Locale string, e.g., en-GB
    value = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)

    user = relationship("UserInDB", back_populates="payments")

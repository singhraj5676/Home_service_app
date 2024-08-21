import uuid
from models.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, ForeignKey


class Review(Base):
    __tablename__ = "review"  # It's conventional to use lowercase table names

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    score = Column(Integer, nullable=False)  # Added nullable=False to ensure a score is always provided
    text = Column(String(1000))
    author_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    receiver_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)

    # Relationships
    author = relationship("UserInDB", foreign_keys=[author_id], back_populates="given_reviews")
    receiver = relationship("UserInDB", foreign_keys=[receiver_id], back_populates="received_reviews")

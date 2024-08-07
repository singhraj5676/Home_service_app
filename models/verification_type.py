# models/verification_type_models.py
from models.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, ForeignKey, Integer


class VerificationType(Base):
    __tablename__ = 'verification_types'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'),nullable=False)

    user = relationship("UserInDB", back_populates="verification_types")

# models/verification_type_models.py
from models.base import Base
from models.user_models import UserInDB
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, ForeignKey, Integer


class VerificationType(Base):
    __tablename__ = 'verification_types'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, nullable=False, unique=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey(UserInDB.id), nullable=False)

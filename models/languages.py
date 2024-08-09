from models.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint


class Language(Base):
    __tablename__ = 'languages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(10), nullable=False)  # ISO 639-1 code
    name = Column(String(100), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)  # Foreign key to user

    # Define the relationship to User
    user = relationship("UserInDB", back_populates="languages")

    # Composite unique constraint
    __table_args__ = (UniqueConstraint('code', 'user_id', name='unique_code_user_id'),)

    def __repr__(self):
        return f"<Language(id={self.id}, code='{self.code}', name='{self.name}', user_id='{self.user_id}')>"

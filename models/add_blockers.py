from models.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, ForeignKey

class AddBlockers(Base):
    __tablename__ = 'add_blockers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    blocker_id = Column(Integer, ForeignKey('blockers.id'), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)

    blocker = relationship("Blockers", back_populates="add_blockers")
    user = relationship("UserInDB", back_populates="add_blockers")

    def __repr__(self):
        return f"<AddBlockers(id={self.id}, blocker_id={self.blocker_id}, user_id={self.user_id})>"



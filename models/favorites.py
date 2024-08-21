from models.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, ForeignKey


class Favourite(Base):
    __tablename__ = "Favourite"

    id = Column(Integer, primary_key=True)
    favors_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    favored_by_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False) # The ID of the user who is adding the other user to their favorites.

    # Relationships
    favors = relationship("UserInDB", foreign_keys=[favors_id], back_populates="adds_to_favorite")
    favored_by = relationship("UserInDB", foreign_keys=[favored_by_id], back_populates="added_by_favorites")

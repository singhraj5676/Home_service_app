from models.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String

class Blockers(Base):
    __tablename__ = 'blockers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, nullable=False)  # 'dog' or 'cat'

    add_blockers = relationship("AddBlockers", back_populates="blocker")

    def __repr__(self):
        return f"<Blockers(id={self.id}, type={self.type})>"

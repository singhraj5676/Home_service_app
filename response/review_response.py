import uuid
from schemas.auth_models import ReviewBase
from pydantic import BaseModel
from typing import Optional

class ReviewResponse(BaseModel):
    id: uuid.UUID

class ReviewGetResponse(BaseModel):
    score: int
    text: Optional[str] = None
    class Config:
        orm_mode = True  
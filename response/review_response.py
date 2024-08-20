import uuid
from schemas.auth_models import ReviewBase
from pydantic import BaseModel

class ReviewResponse(BaseModel):
    id: uuid.UUID


    class Config:
        orm_mode = True  
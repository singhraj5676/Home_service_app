from typing import Optional
from pydantic import BaseModel

class VerificationType_Response(BaseModel):
    type: Optional[str] = None

    class Config:
        orm_mode = True
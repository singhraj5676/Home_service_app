from typing import Optional
from pydantic import BaseModel


class Language_Response(BaseModel):
    code: str
    name: str
    
    class Config:
        orm_mode = True



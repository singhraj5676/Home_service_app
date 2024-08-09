from typing import Optional
from pydantic import BaseModel

class Currency_Response(BaseModel):
    code: str
    name: str
    symbol: Optional[str] = None

    class Config:
        orm_mode = True
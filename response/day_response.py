from pydantic import BaseModel

class Day_Response(BaseModel):
    name: str

    class Config:
        orm_mode = True

from typing import Optional
from pydantic import BaseModel


class Location_Response(BaseModel):
    address: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    city: str
    slug: Optional[str] = None
    country: str
    country_code: str
    place_id: Optional[str] = None

    class Config:
        orm_mode = True
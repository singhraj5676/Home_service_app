import uuid
from typing import Optional,List
from datetime import datetime
from pydantic import BaseModel
from response.location_response import Location_Response
from response.verification_response import VerificationType_Response

class User_Response(BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: Optional[str] = None
    email: str
    phone_number: Optional[str] = None
    is_verified: bool
    is_online: bool
    is_suspended: bool
    last_login: Optional[datetime] = None
    location: Optional[Location_Response] = None  # Add location field
    verification_types: Optional[List[VerificationType_Response]] = None


    class Config:
        orm_mode = True


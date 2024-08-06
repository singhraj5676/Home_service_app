# models/auth_models.py
import uuid
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    email: str | None = None

class User_Response(BaseModel):
    id: uuid.UUID

class UserInDB(User_Response):
    hashed_password: str


class UserCreate(BaseModel):
    email: str
    password: str
    phone_number: Optional[str] = None


class User_Update(BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: Optional[str] = None
    email: str
    hashed_password: str
    disabled: bool = False
    is_verified: bool = False
    is_online: bool = False
    is_suspended: bool = False
    score: Optional[float] = None
    votes: Optional[int] = None
    phone_number: Optional[str] = None
    domain: Optional[str] = None
    domain_language: Optional[str] = None
    last_login: Optional[datetime] = None

    class Config:
        orm_mode = True

class User_Base(BaseModel): 
    first_name: str
    email: str
    last_name: str
    password: str
    phone_number: Optional[str] = None
    domain: Optional[str] = None
    domain_language: Optional[str] = None
    disabled: Optional[bool] = None

class LocationCreate(BaseModel):
    address: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    city: str
    slug: Optional[str] = None
    country: str
    country_code: str
    place_id: Optional[str] = None


class UserProfileUpdate(BaseModel):
    max_distance: Optional[int] = None
    currency: Optional[str] = None
    amount: Optional[int] = None
    experience: Optional[int] = None
    personal_note: Optional[str] = None
    published: Optional[bool] = None
    user_alert: Optional[bool] = None
    personal_message: Optional[bool] = None
    duration: Optional[int] = None
    registered_date: Optional[int] = None
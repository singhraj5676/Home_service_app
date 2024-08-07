from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from models.user_models import UserInDB
from models.user_profile import UserProfile
from models.locations import Location
from schemas.auth_models import User_Update, UserProfileUpdate, LocationCreate
from fastapi import HTTPException, status
from uuid import UUID

def update_user_details(db: Session, user_update: User_Update):
    try:
        user = db.query(UserInDB).filter(UserInDB.id == user_update.id).one()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.first_name = user_update.first_name
    user.last_name = user_update.last_name
    user.email = user_update.email
    user.disabled = user_update.disabled
    user.is_verified = user_update.is_verified
    user.is_online = user_update.is_online
    user.is_suspended = user_update.is_suspended
    user.score = user_update.score
    user.votes = user_update.votes
    user.phone_number = user_update.phone_number
    user.domain = user_update.domain
    user.domain_language = user_update.domain_language
    user.last_login = user_update.last_login

    db.commit()
    db.refresh(user)

def update_user_profile(db: Session, user_id: UUID, user_profile_update: UserProfileUpdate):
    user_profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if not user_profile:
        user_profile = UserProfile(user_id=user_id)
        db.add(user_profile)
    
    user_profile.max_distance = user_profile_update.max_distance
    user_profile.currency = user_profile_update.currency
    user_profile.amount = user_profile_update.amount
    user_profile.experience = user_profile_update.experience
    user_profile.personal_note = user_profile_update.personal_note
    user_profile.published = user_profile_update.published
    user_profile.user_alert = user_profile_update.user_alert
    user_profile.personal_message = user_profile_update.personal_message
    user_profile.duration = user_profile_update.duration
    user_profile.registered_date = user_profile_update.registered_date

    db.commit()
    db.refresh(user_profile)

def update_location(db: Session, user_id: UUID, location_create: LocationCreate):
    location = db.query(Location).filter(Location.user_id == user_id).first()
    if not location:
        location = Location(user_id=user_id)
        db.add(location)
    
    location.address = location_create.address
    location.latitude = location_create.latitude
    location.longitude = location_create.longitude
    location.city = location_create.city
    location.slug = location_create.slug
    location.country = location_create.country
    location.country_code = location_create.country_code
    location.place_id = location_create.place_id

    db.commit()
    db.refresh(location)

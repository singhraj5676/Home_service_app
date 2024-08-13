from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from models.user_models import UserInDB
from models.user_profile import UserProfile
from models.locations import Location
from models.currency import Currency
from models.languages import Language
from models.blockers import Blockers
from models.available_day  import AvailableDay
from models.add_blockers import AddBlockers
from models.day import Days
from schemas.auth_models import User_Update, UserProfileUpdate, LocationCreate , UserCurrrencyCreate, UserLanguageCreate 
from fastapi import HTTPException, status
from uuid import UUID
from typing import List
import uuid
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

# def update_user_profile(db: Session, user_id: UUID, user_profile_update: UserProfileUpdate):
#     user_profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
#     if not user_profile:
#         user_profile = UserProfile(user_id=user_id)
#         db.add(user_profile)
    
#     user_profile.max_distance = user_profile_update.max_distance
#     user_profile.currency = user_profile_update.currency
#     user_profile.amount = user_profile_update.amount
#     user_profile.experience = user_profile_update.experience
#     user_profile.personal_note = user_profile_update.personal_note
#     user_profile.published = user_profile_update.published
#     user_profile.user_alert = user_profile_update.user_alert
#     user_profile.personal_message = user_profile_update.personal_message
#     user_profile.duration = user_profile_update.duration
#     user_profile.registered_date = user_profile_update.registered_date
#     user_profile.role = user_profile_update.role

#     db.commit()
#     db.refresh(user_profile)
def update_user_profile(db: Session, user_id: UUID, user_profile_update: UserProfileUpdate):
    
    user_profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

    if not user_profile:
        user_profile = UserProfile(
            user_id=user_id,
            max_distance=user_profile_update.max_distance,
            currency=user_profile_update.currency,
            amount=user_profile_update.amount,
            experience=user_profile_update.experience,
            personal_note=user_profile_update.personal_note,
            published=user_profile_update.published,
            user_alert=user_profile_update.user_alert,
            personal_message=user_profile_update.personal_message,
            duration=user_profile_update.duration,
            registered_date=user_profile_update.registered_date,
            role=user_profile_update.role
        )
        db.add(user_profile)
    else:
        # Update existing entry
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
        user_profile.role = user_profile_update.role
    
    db.commit()
    db.refresh(user_profile)

def update_location(db: Session, user_id: UUID, location_create: LocationCreate):
    # Check if the required fields are present
    if not location_create.address or not location_create.city:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Address and city are required")

    # Query for existing location entry
    location = db.query(Location).filter(Location.user_id == user_id).first()

    if not location:
        # Create a new entry if it does not exist
        location = Location(
            user_id=user_id,
            address=location_create.address,
            latitude=location_create.latitude,
            longitude=location_create.longitude,
            city=location_create.city,
            slug=location_create.slug,
            country=location_create.country,
            country_code=location_create.country_code,
            place_id=location_create.place_id
        )
        db.add(location)
    else:
        # Update existing entry
        location.address = location_create.address
        location.latitude = location_create.latitude
        location.longitude = location_create.longitude
        location.city = location_create.city
        location.slug = location_create.slug
        location.country = location_create.country
        location.country_code = location_create.country_code
        location.place_id = location_create.place_id

    # Commit the transaction and refresh the instance
    db.commit()
    db.refresh(location)

def update_currency(db: Session, user_id: UUID, currency_create: UserCurrrencyCreate):
    if not currency_create.code or not currency_create.name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Currency code and name are required")
    
    currency = db.query(Currency).filter(Currency.user_id == user_id).first()
    if not currency:
        currency = Currency(user_id=user_id, code=currency_create.code, name=currency_create.name, symbol=currency_create.symbol)
        db.add(currency)
    else:
        currency.code = currency_create.code
        currency.name = currency_create.name
        currency.symbol = currency_create.symbol

    db.commit()
    db.refresh(currency)


def update_language(db: Session, user_id: UUID, language_create: UserLanguageCreate):
    if not language_create.code  or not language_create.name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Language code and name are required")
    
    language = db.query(Language).filter(Language.user_id==user_id).first()

    if not language:
        language = Language(user_id=user_id, code=language_create.code, name=language_create.name)
        db.add(language)
    else:
        language.code = language_create.code
        language.name = language_create.name
    db.commit()
    db.refresh(language)

def update_available_days(
    db: Session, user_id: UUID, day_names: List[str]
):
    # Get the IDs of the days to be added
    day_ids = db.query(Days.id).filter(Days.name.in_(day_names)).all()
    print(day_ids)
    
    if not day_ids:
        raise HTTPException(status_code=400, detail="No valid days provided")

    day_ids = [day_id for (day_id,) in day_ids]  # Convert list of tuples to list of IDs

    # Delete existing available days for this user
    db.query(AvailableDay).filter(AvailableDay.user_id == user_id).delete()

    # Add new available days
    for day_id in day_ids:
        available_day = AvailableDay(day_id=day_id, user_id=user_id)
        db.add(available_day)

    db.commit()

def add_update_blockers(db: Session, user_id: UUID, blockers: List[str]):
    print('blockers',blockers)
    

    capitalized_blockers = [blocker.capitalize() for blocker in blockers]
    print('capitalized_blockers',capitalized_blockers)
    # Get the IDs of the blockers to be added
    blockers_ids = db.query(Blockers.id).filter(Blockers.type.in_(capitalized_blockers)).all()
    print('blo',blockers_ids)

    if not blockers_ids:
        raise HTTPException(status_code=400, detail="No valid blockers provided")
    
    blockers_ids = [blocker_id for (blocker_id,) in blockers_ids]
    print('-----',blockers_ids)

    db.query(AddBlockers).filter(AddBlockers.user_id == user_id).delete()

    for blocker_id in blockers_ids:
        blocker_opt = AddBlockers(blocker_id=blocker_id , user_id = user_id)
        db.add(blocker_opt)
    
    db.commit()
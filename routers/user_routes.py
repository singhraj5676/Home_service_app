#routers/user_routes.py

import uuid
import smtplib
from uuid import uuid4
from fastapi import Request
from database import get_db
from twilio.rest import Client
from .main_router import router
from auth import get_password_hash
from sqlalchemy.orm import Session
from email.mime.text import MIMEText
from models.locations import Location
from models.user_models import UserInDB
from datetime import datetime, timedelta
from auth import (get_current_active_user)
from models.user_profile import UserProfile
from typing import Optional, Annotated, List
from response.user_response import User_Response
from fastapi import Depends, HTTPException, status
from consts.const import EMAIL_PASSWORD, EMAIL_USER
from models.verification_type import VerificationType
from models.verification_token import VerificationToken
from schemas.auth_models import (UserCreate, User_Update, UserProfileUpdate, LocationCreate,
                                 User_Registration_Response , UserCurrrencyCreate, UserLanguageCreate)
from profile_update_service import (update_user_details, update_user_profile, update_location, update_currency, 
                                    update_language, update_available_days, add_update_blockers, create_user_response)


from response.location_response import Location_Response
from utils.helper_func import *

@router.post("/register", response_model=User_Registration_Response)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_email = db.query(UserInDB).filter(UserInDB.email == user.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash the password
    hashed_password = get_password_hash(user.password)

    # Create a new user     
    new_user = UserInDB(
        email=user.email,
        hashed_password=hashed_password,
        phone_number=user.phone_number if user.phone_number else None,  # Set phone_number to None if not provided
        is_verified=False
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Generate and send verification token
    email_token = generate_verification_token(new_user.id, db, "email")
    send_verification_email(new_user.email, email_token)
    
    if user.phone_number:
        sms_token = generate_verification_token(new_user.id, db, "sms")
        send_verification_sms(user.phone_number, sms_token)  # Assuming user.phone_number is available


    return new_user

def generate_verification_token(user_id: uuid.UUID, db: Session, verification_type: str):
    token = str(uuid4())
    expiration = datetime.utcnow() + timedelta(hours=24)  # Token valid for 24 hours
    verification_token = VerificationToken(
        token=token,
        expiration=expiration,
        user_id=user_id,
        type=verification_type
    )
    db.add(verification_token)
    db.commit()
    
    return token

def send_verification_email(email: str, token: str):
    print(email, token)
    verification_link = f"http://yourapp.com/verify/{token}"
    message = MIMEText(f"Please verify your email by clicking the following link: {verification_link}")
    message['Subject'] = 'Email Verification'
    message['From'] = 'rajps@infusionanalysts.com'
    message['To'] = email

    # try:
    with smtplib.SMTP('smtp.gmail.com', port=587) as server:
        server.starttls()  # Secure the connection
        server.login(EMAIL_USER, EMAIL_PASSWORD)  # If authentication is needed
        server.send_message(message)
    print(f"Verification email sent to {email}")
    # except Exception as e:
    #     print(f"Failed to send email: {e}")


def send_verification_sms(phone_number: str, token: str):
    pass
    # verification_link = f"http://yourapp.com/verify/{token}"
    # message_body = f"Please verify your phone number by clicking the following link: {verification_link}"

    # # Twilio setup
    # account_sid = 'your_twilio_account_sid'
    # auth_token = 'your_twilio_auth_token'
    # client = Client(account_sid, auth_token)

    # message = client.messages.create(
    #     body=message_body,
    #     from_='your_registered_sender_id',  # Replace with your registered Sender ID
    #     to=phone_number
    # )

    # return message


@router.get("/verify/{token}", response_model=User_Registration_Response)
def verify_token(token: str, db: Session = Depends(get_db)):
    verification = db.query(VerificationToken).filter(VerificationToken.token == token).first()
    if verification is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
    if verification.expiration < datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token expired")

    user = db.query(UserInDB).filter(UserInDB.id == verification.user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Verify the user
    user.is_verified = True
    db.commit()

    # Optionally delete the token after verification
    db.delete(verification)
    db.commit()

    # Save the verification type
    verification_type = db.query(VerificationType).filter(
        VerificationType.user_id == user.id, VerificationType.type == verification.type
    ).first()

    if not verification_type:
        verification_type = VerificationType(user_id=user.id, type=verification.type)
        db.add(verification_type)
        db.commit()

    return user

@router.post("/resend-verification")
def resend_verification(user_id: uuid.UUID, verification_type: str, db: Session = Depends(get_db)):
    user = db.query(UserInDB).filter(UserInDB.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    verification = db.query(VerificationToken).filter(
        VerificationToken.user_id == user_id, VerificationToken.type == verification_type
    ).first()

    if verification:
        db.delete(verification)
        db.commit()

    token = generate_verification_token(user_id, db, verification_type)

    if verification_type == "email":
        send_verification_email(user.email, token)
    elif verification_type == "sms":
        send_verification_sms(user.phone_number, token)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid verification type")

    return {"message": "Verification token resent"}


@router.post("/update-login")
def update_last_login(user_id: uuid.UUID, db: Session = Depends(get_db)):
    print('hii')
    user = db.query(UserInDB).filter(UserInDB.id == user_id).first()
    if user:
        user.last_login = datetime.utcnow()
        db.commit()
        db.refresh(user)
        return {"message": "Last login updated"}
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.post("/update-profile")
async def update_profile(
    request: Request,
    user_update: User_Update,
    user_profile_update: Optional[UserProfileUpdate] = None,
    location_create: Optional[LocationCreate] = None,
    currency_create: Optional[UserCurrrencyCreate] = None,
    language_create: Optional[UserLanguageCreate] = None,
    # available_days_create: Optional[AvailableDays] = None,
    available_days: Optional[List[str]] = None,  # Changed to List[str]
    add_blockers: Optional[List[str]] = None,

    db: Session = Depends(get_db)
):
    raw_body = await request.body()
    print("Raw request body:", raw_body.decode("utf-8"))

    # Continue with your route logic
    print("Available days:", available_days)

    # Update user details
    update_user_details(db, user_update)
    
    # Update or create user profile
    if user_profile_update:
        update_user_profile(db, user_update.id, user_profile_update)
    
    # Update or create location
    if location_create:
        update_location(db, user_update.id, location_create)

    # Update or create currency
    if currency_create:
        update_currency(db, user_update.id, currency_create)
    
    # Update or create language
    if language_create:
        update_language(db, user_update.id, language_create)

    # Update available days
    if available_days:
        update_available_days(db, user_update.id, available_days)

    if add_blockers:
        print(f"Updating blockers for user_id: {add_blockers}")
        add_update_blockers(db, user_update.id, add_blockers)

    return {"message": "User details, profile, and location updated successfully"}


@router.get("/{user_id}", response_model=User_Response)
def get_user_by_id(
    user_id: uuid.UUID,
    # current_user: Annotated[User_Response, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    # if current_user.id != user_id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this user")
    
    user = db.query(UserInDB).filter(UserInDB.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Create a User_Response object using the updated function
    response = create_user_response(user, db)

    return response

@router.get("/city/{city}", response_model=List[User_Response])
def get_users_by_city(city: str, db: Session = Depends(get_db)):
    # Query users based on city
    users = db.query(UserInDB).join(Location).filter(Location.city == city).all()
    
    if not users:
        raise HTTPException(status_code=404, detail="No users found in this city")
    
    user_responses = [create_user_response(user, db) for user in users]

    return user_responses

@router.get("/slug/{slug}", response_model=List[User_Response])
def get_users_by_slug(slug: str, db: Session = Depends(get_db)):
    # Query users based on city
    users = db.query(UserInDB).join(Location).filter(Location.slug == slug).all()
    
    if not users:
        raise HTTPException(status_code=404, detail="No users found in this slug")
    
    user_responses = [create_user_response(user, db) for user in users]

    return user_responses

@router.get("/get_workers_by_slug/{slug}", response_model=List[User_Response])
def get_workers_by_slug(
    slug: str,
    db: Session = Depends(get_db)
):  
    # Query workers based on slug
    workers = (
        db.query(UserInDB)
        .join(UserProfile)
        .join(Location)
        .filter(UserProfile.role == "worker", Location.slug == slug)
        .all()
    )
    
    if not workers:
        raise HTTPException(status_code=404, detail="No workers found with this slug")
    
    return workers

@router.get("/get_customers_by_slug/{slug}", response_model=List[User_Response])
def get_customers_by_slug(
    slug: str,
    db: Session = Depends(get_db)
):
    customers = (
        db.query(UserInDB)
        .join(UserProfile)
        .join(Location)
        .filter(UserProfile.role == "customer", Location.slug == slug)
        .all()
    )

    if not customers:
        raise HTTPException(status_code=404, detail="No customers found with this slug")
    
    user_responses = [create_user_response(user, db) for user in customers]
    return user_responses


@router.get("/locations", response_model=List[Location_Response])
def get_locations_by_partial_address(partial_address: str, db: Session = Depends(get_db)):
    locations = db.query(Location).filter(Location.address.ilike(f"%{partial_address}%")).all()
    
    if not locations:
        raise HTTPException(status_code=404, detail="No locations found with this partial address")

    location_responses = [convert_location(location) for location in locations]

    return location_responses

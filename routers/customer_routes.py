from database import get_db
from sqlalchemy import func
from models.day import Days
from typing import List, Optional
from sqlalchemy.orm import Session
from models.currency import Currency
from models.currency import Currency
from models.locations import Location
from models.languages import Language
from models.user_models import UserInDB
from models.user_profile import UserProfile
from models.available_day import AvailableDay
from response.user_response import User_Response
from profile_update_service import create_user_response
from fastapi import APIRouter, Query, Depends, HTTPException



router = APIRouter()

def apply_criteria_filters(
    query: Session,
    amount: Optional[int] = None,
    currency: Optional[str] = None,
    languages: Optional[List[str]] = None,
    days: Optional[List[str]] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    max_distance: Optional[float] = None
):
    query = query.join(UserProfile).join(Location)

    if amount is not None:
        query = query.filter(UserProfile.amount >= amount)
    
    if currency is not None:
        query = query.join(Currency).filter(Currency.code == currency)
    
    if languages:
        query = query.join(Language).filter(Language.code.in_(languages))
    
    if days:
        query = query.join(AvailableDay).join(Days).filter(Days.name.in_(days))
    
    if latitude is not None and longitude is not None:
        query = query.filter(
            Location.latitude >= latitude,
            Location.longitude >= longitude
        )
        
        if max_distance is not None:
            latitude_tolerance = 0.4
            longitude_tolerance = 0.4

            query = query.filter(
                Location.latitude.between(latitude - latitude_tolerance, latitude + latitude_tolerance),
                Location.longitude.between(longitude - longitude_tolerance, longitude + longitude_tolerance)
            )

            query = query.filter(
                func.ST_DistanceSphere(
                    func.ST_MakePoint(Location.longitude, Location.latitude),
                    func.ST_MakePoint(longitude, latitude)
                ) <= max_distance * 1000  # converting km to meters
            )
    
    return query


@router.get("/get_customers_by_criteria", response_model=List[User_Response])
def get_customers_by_criteria(
    amount: Optional[int] = Query(None),
    currency: Optional[str] = Query(None),
    languages: Optional[List[str]] = Query(None),
    days: Optional[List[str]] = Query(None),
    latitude: Optional[float] = Query(None),
    longitude: Optional[float] = Query(None),
    max_distance: Optional[float] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(UserInDB)
    
    # Apply filters
    query = apply_criteria_filters(
        query,  
        amount=amount,
        currency=currency,
        languages=languages,
        days=days,
        latitude=latitude,
        longitude=longitude,
        max_distance=max_distance
    )
    
    # Apply ordering
    order_type = "score"
    order_direction = "desc"
    if hasattr(UserInDB, order_type):
        order_column = getattr(UserInDB, order_type)
        query = query.order_by(order_column.desc() if order_direction == "desc" else order_column.asc())
    else:
        query = query.order_by(UserInDB.score.desc())  # Default order
    
    # Retrieve customers
    customers = query.all()

    if not customers:
        raise HTTPException(status_code=404, detail="No customers found with the given criteria")
    
    user_responses = [create_user_response(user, db) for user in customers]
    
    return user_responses

@router.get("/count", response_model=int)
def get_customers_count_by_criteria(
    amount: Optional[int] = Query(None),
    currency: Optional[str] = Query(None),
    languages: Optional[List[str]] = Query(None),
    days: Optional[List[str]] = Query(None),
    latitude: Optional[float] = Query(None),
    longitude: Optional[float] = Query(None),
    max_distance: Optional[float] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(func.count(UserInDB.id))
    
    # Apply filters
    query = apply_criteria_filters(
        query, 
        amount=amount,
        currency=currency,
        languages=languages,
        days=days,
        latitude=latitude,
        longitude=longitude,
        max_distance=max_distance
    )
    
    # Get the count of customers
    count = query.scalar() 

    return count

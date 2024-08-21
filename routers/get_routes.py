#get_routes.py
from typing import List
from database import get_db
from utils.helper_func import *
from sqlalchemy.orm import Session
from fastapi import APIRouter, Query
from fastapi import Depends, HTTPException
from response.location_response import Location_Response


from models.locations import Location

router = APIRouter()

@router.get("/test", response_model=List[str])
def test_query_param(param: str = Query(...)):
    return [param]


@router.get("/locations", response_model=List[Location_Response])
def get_locations_by_partial_address(partial_address: str = Query(...), db: Session = Depends(get_db)):
    print(f"Received partial address: {partial_address}")  # Debugging line
    locations = db.query(Location).filter(Location.address.ilike(f"%{partial_address}%")).all()
    
    if not locations:
        raise HTTPException(status_code=404, detail="No locations found with this partial address")

    location_responses = [convert_location(location) for location in locations]

    return location_responses


# @router.get("/locations/{place_id}", response_model=Location_Response)
# def get_locations_by_place_id(place_id: str, db: Session = Depends(get_db)):
#     location = db.query(Location).filter(Location.place_id == place_id).first()
    
#     if not location:
#         raise HTTPException(status_code=404, detail="No locations found with this partial address")

#     return  convert_location(location)

@router.get("/locations/by_place_id", response_model=Location_Response)
def get_location_by_place_id(place_id: str = Query(...), db: Session = Depends(get_db)):
    location = db.query(Location).filter(Location.place_id == place_id).first()
    
    if not location:
        raise HTTPException(status_code=404, detail="No location found with this place_id")

    return convert_location(location)

@router.get("/locations/by_slug", response_model=Location_Response)
def get_location_by_slug(slug: str = Query(...), db: Session = Depends(get_db)):
    location = db.query(Location).filter(Location.slug == slug).first()
    
    if not location:
        raise HTTPException(status_code=404, detail="Location not found with this slug")

    return convert_location(location)



@router.get("/locations/by_lat_lng", response_model=List[Location_Response])
def get_locations_by_lat_lng(
    latitude: float = Query(..., description="Latitude of the location"),
    longitude: float = Query(..., description="Longitude of the location"),
    db: Session = Depends(get_db)
):
    # Define a tolerance range for matching coordinates (if needed)
    tolerance = 0.0001  # Example tolerance value

    # Query the database for locations within the tolerance range of the given latitude and longitude
    locations = db.query(Location).filter(
        Location.latitude.between(latitude - tolerance, latitude + tolerance),
        Location.longitude.between(longitude - tolerance, longitude + tolerance)
    ).all() 

    if not locations:
        raise HTTPException(status_code=404, detail="No locations found with the provided latitude and longitude")

    location_responses = [convert_location(location) for location in locations]

    return location_responses


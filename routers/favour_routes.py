from database import get_db
from auth import get_current_user
from sqlalchemy.orm import Session
from models.user_models import UserInDB
from models.favorites  import Favourite
from schemas.auth_models import FavoriteAction
from fastapi import APIRouter, Depends, HTTPException


router = APIRouter()

# @router.post("/favorites/")
@router.post("/")
async def manage_favorites(
    favorite_action: FavoriteAction,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    # Check if the user to be favored exists
    user_to_favor = db.query(UserInDB).filter(UserInDB.id == favorite_action.favorite_id).first()

    if not user_to_favor:
        raise HTTPException(status_code=404, detail="User not found")

    current_user_id = current_user.id

    if favorite_action.action == "add":
        # Check if the favorite relationship already exists
        existing_favorite = db.query(Favourite).filter(
            Favourite.favors_id == favorite_action.favorite_id,
            Favourite.favored_by_id == current_user_id
        ).first()

        if existing_favorite:
            raise HTTPException(status_code=400, detail="Favorite already exists")

        # Create a new favorite entry
        new_favorite = Favourite(favors_id=favorite_action.favorite_id, favored_by_id=current_user_id)
        db.add(new_favorite)
        db.commit()

        return {"detail": "User added to favorites successfully"}

    elif favorite_action.action == "remove":
        # Find the favorite relationship
        existing_favorite = db.query(Favourite).filter(
            Favourite.favors_id == favorite_action.favorite_id,
            Favourite.favored_by_id == current_user_id
        ).first()

        if not existing_favorite:
            raise HTTPException(status_code=404, detail="Favorite not found")

        # Remove the favorite relationship
        db.delete(existing_favorite)
        db.commit()

        return {"detail": "User removed from favorites successfully"}

    else:
        raise HTTPException(status_code=400, detail="Invalid action")

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.favorites  import Favourite
from database import get_db
from schemas.auth_models import FavoriteAction
from 

router = APIRouter()

@router.post("/favorites/")
def manage_favorites(
    favorite_action: FavoriteAction,
    current_user: UserInDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_to_favor = db.query(UserInDB).filter(UserInDB.id == favorite_action.favorite_id).first()

    if not user_to_favor:
        raise HTTPException(status_code=404, detail="User not found")  

    current_user_id = current_user.id 

    if favorite_action.action == "add":

        existing_favorites = db.query(Favourite).filter(Favourite.favors_id == favorite_action.favorite_id,
                                                        Favourite.favored_by_id == current_user_id).first()
        
        if existing_favorites:
            raise HTTPException(status_code=400, detail="User already in favorites")
        
        
        new_favorite = Favourite(favors_id=favorite_action.favorite_id, favored_by_id=current_user_id)
        db.add(new_favorite)
        db.commit()
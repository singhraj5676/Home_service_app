# routers/auth_routes.py
import datetime
from database import get_db
from typing import Annotated
from datetime import timedelta
from .main_router import router
from sqlalchemy.orm import Session
from models.user_models import UserInDB
from schemas.auth_models import Token, User_Response
from fastapi import  Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from models.verification_models import VerificationToken
from auth import (authenticate_user, create_access_token, get_current_active_user,ACCESS_TOKEN_EXPIRE_MINUTES)


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not verified",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username,"email": user.email }, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me/", response_model=User_Response)
def read_users_me(
    current_user: Annotated[User_Response, Depends(get_current_active_user)],
):
    print(current_user)
    print('getting user')
    return current_user

@router.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User_Response, Depends(get_current_active_user)],
):
    return [{"item_id": current_user.id, "owner": current_user.username}]


# routers/auth_routes.py
@router.get("/verify/{token}", response_model=User_Response)
async def verify_token(token: str, db: Session = Depends(get_db)):
    verification = db.query(VerificationToken).filter(VerificationToken.token == token).first()
    if verification is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
    if verification.expiration < datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token expired")

    user = db.query(UserInDB).filter(UserInDB.id == verification.user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.disabled = False
    db.delete(verification)  # Remove the token after verification
    db.commit()

    return user


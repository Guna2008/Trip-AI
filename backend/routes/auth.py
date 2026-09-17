from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..schemas import UserCreate, UserResponse, Token
from ..core.security import (hash_password, verify_password, create_access_token)
from ..dependencies import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate,db: Session = Depends(get_db)):
    existing_user = db.query(User).filter((User.username == user_data.username) | (User.email == user_data.email)).first()

    if existing_user:
        raise HTTPException(status_code=400,detail="Username or email already exists")

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):

    user = db.query(User).filter(User.username == form_data.username).first()

    if not user or not verify_password(form_data.password,user.hashed_password):
        raise HTTPException(status_code=401,detail="Invalid username or password")

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.user import UserCreate, UserResponse
from app.crud.user import create_user, get_user

router = APIRouter()

@router.post("/create)", response_model=UserResponse)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

@router.get("/{user_id}:", response_model=UserResponse)
def create_user_endpoint(user_id, db: Session = Depends(get_db)):
    return get_user(db, user_id)

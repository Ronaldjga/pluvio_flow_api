from typing import Annotated
from sqlalchemy.orm import Session

from app.core.auth import get_current_user

# FASTAPI
from fastapi import APIRouter, Depends, status

# DATABASE
from app.database.session import get_db

# AUTH SCHEMA
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.schemas.user import UserResponse

# SERVICE IMPORTS
from app.services.auth_service import AuthService


# REPOSITORIES
from app.repositories.user_repository import UserRepository


router = APIRouter()
Current_session = Annotated[Session, Depends(get_db)]


# PROVIDERS
def get_user_repository(db: Current_session):
    return UserRepository(db)


User_repo = Annotated[UserRepository, Depends(get_user_repository)]


def get_auth_service(userRepository: User_repo):
    return AuthService(userRepository)


Auth_service = Annotated[AuthService, Depends(get_auth_service)]


# ENDPOINTS
@router.post("/sign-up", response_model=TokenResponse, status_code=201)
def register(data: RegisterRequest, auth_service: Auth_service):
    return auth_service.register_user(
        data.name, data.username, data.email, data.cpf, data.password
    )


@router.post("/sign-in", response_model=TokenResponse)
def login(data: LoginRequest, auth_service: Auth_service):
    return auth_service.authenticate_user(data.username, data.password)


@router.get("/verify", response_model=UserResponse, status_code=status.HTTP_200_OK)
def verify_token(current_user=Depends(get_current_user)):
    return current_user

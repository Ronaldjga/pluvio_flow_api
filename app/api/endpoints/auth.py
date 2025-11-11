from typing import Annotated
from sqlalchemy.orm import Session

# FASTAPI
from fastapi import APIRouter, Depends

# DATABASE
from app.database.session import get_db

# MODELS
from app.models.user import User

# AUTH SCHEMA
from app.schemas.auth import LoginRequest, RegisterRequest

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
@router.post("/sign-up", status_code=201)
def register(data: RegisterRequest, auth_service: Auth_service):
    """Registra um novo usuário e retorna o token JWT."""
    return auth_service.register_user(data.name, data.username, data.email, data.cpf, data.password)


@router.post("/sign-in")
def login(data: LoginRequest, auth_service: Auth_service):
    """Autentica o usuário e retorna o token JWT."""
    return auth_service.authenticate_user(data.username, data.password)

from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.repositories.user_repository import UserRepository
from app.repositories.occurrence_repository import OccurrenceRepository
from app.services.auth_service import AuthService
from app.services.occurrence_service import OccurrenceService

# Sessão
Current_session = Annotated[Session, Depends(get_db)]

# Repositórios
def get_user_repository(db: Current_session):
    return UserRepository(db)
User_repo = Annotated[UserRepository, Depends(get_user_repository)]

def get_occurrence_repository(db: Current_session):
    return OccurrenceRepository(db)
Occurrence_repo = Annotated[OccurrenceRepository, Depends(get_occurrence_repository)]

# Serviços
def get_auth_service(user_repo: User_repo):
    return AuthService(user_repo)
Auth_service = Annotated[AuthService, Depends(get_auth_service)]

def get_occurrence_service(repo: Occurrence_repo):
    return OccurrenceService(repo)
Occurrence_service = Annotated[OccurrenceService, Depends(get_occurrence_service)]

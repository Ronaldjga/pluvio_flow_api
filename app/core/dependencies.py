from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.repositories.user_repository import UserRepository
from app.repositories.occurrence_repository import OccurrenceRepository
from app.repositories.insight_repository import InsightRepository  # NOVO
from app.services.auth_service import AuthService
from app.services.occurrence_service import OccurrenceService
from app.services.insight_service import InsightService  # NOVO

# Sessão
Current_session = Annotated[Session, Depends(get_db)]


# Repositórios
def get_user_repository(db: Current_session):
    return UserRepository(db)


User_repo = Annotated[UserRepository, Depends(get_user_repository)]


def get_occurrence_repository(db: Current_session):
    return OccurrenceRepository(db)


Occurrence_repo = Annotated[OccurrenceRepository, Depends(get_occurrence_repository)]


# NOVO: Insight Repository
def get_insight_repository(db: Current_session):
    return InsightRepository(db)


Insight_repo = Annotated[InsightRepository, Depends(get_insight_repository)]


# Serviços
def get_auth_service(user_repo: User_repo):
    return AuthService(user_repo)


Auth_service = Annotated[AuthService, Depends(get_auth_service)]


def get_occurrence_service(repo: Occurrence_repo):
    return OccurrenceService(repo)


Occurrence_service = Annotated[OccurrenceService, Depends(get_occurrence_service)]


# NOVO: Insight Service
def get_insight_service(insight_repo: Insight_repo):
    return InsightService(insight_repo)


Insight_service = Annotated[InsightService, Depends(get_insight_service)]

from typing import Annotated
from sqlalchemy.orm import Session

from app.core.auth import get_current_user

# FASTAPI
from fastapi import APIRouter, Depends, status

# DATABASE
from app.database.session import get_db

# MODELS
from app.models.user import User

# AUTH SCHEMA
from app.schemas.occurrence import OccurrenceCreate

# SERVICE IMPORTS
from app.services.occurrence_service import OccurrenceService


# REPOSITORIES
from app.repositories.occurrence_repository import OccurrenceRepository


router = APIRouter()
Current_session = Annotated[Session, Depends(get_db)]


# --- Repository provider ---
def get_occurrence_repository(db: Current_session):
    return OccurrenceRepository(db)


Occurrence_repo = Annotated[OccurrenceRepository, Depends(get_occurrence_repository)]


# --- Service provider ---
def get_occurrence_service(repo: Occurrence_repo):
    return OccurrenceService(repo)


Occurrence_service = Annotated[OccurrenceService, Depends(get_occurrence_service)]

# --- Authenticated user ---
Current_user = Annotated[User, Depends(get_current_user)]


# --- Routes ---
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_occurrence(
    data: OccurrenceCreate,
    current_user: Current_user,
    occurrence_service: Occurrence_service,
):
    """Cria uma nova ocorrência associada ao usuário logado."""
    return occurrence_service.create_occurrence(current_user.id, data)


@router.get("/geojson")
def list_occurrences(occurrence_service: Occurrence_service):
    """Lista todas as ocorrências em formato GeoJSON, com username do autor."""
    return occurrence_service.list_occurrences_geojson()

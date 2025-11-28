from typing import Annotated
from fastapi import APIRouter, Depends

# Schemas
from app.schemas.insight import InsightResponse

# Services
from app.services.insight_service import InsightService

# Dependencies
from app.core.dependencies import Insight_service

router = APIRouter()


@router.get("", response_model=InsightResponse)
def get_insights(insight_service: Insight_service):
    """
    Retorna insights e estatísticas sobre as ocorrências.
    """
    return insight_service.get_insights()

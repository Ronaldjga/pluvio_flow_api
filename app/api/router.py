from fastapi import APIRouter
from app.api.endpoints import (
    auth,
    occurrence
)

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(occurrence.router, prefix="/occurrence", tags=["occurrence"])

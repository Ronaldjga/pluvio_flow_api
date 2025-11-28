from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class OccurrenceBase(BaseModel):
    name: str = Field(..., description="Nome da ocorrência")
    category: str = Field(..., description="Categoria: lixo, enchente, etc.")
    description: Optional[str] = Field(None, description="Descrição detalhada")
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

class OccurrenceCreate(OccurrenceBase):
    pass

class OccurrenceResponse(OccurrenceBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


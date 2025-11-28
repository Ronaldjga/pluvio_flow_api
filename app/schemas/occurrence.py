from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class SeverityResponse(BaseModel):
    id: int
    code: str
    name: str
    color: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class OccurrenceBase(BaseModel):
    name: str = Field(..., description="Nome da ocorrência")
    category: str = Field(..., description="Categoria: lixo, enchente, etc.")
    description: Optional[str] = Field(None, description="Descrição detalhada")
    severity_id: int = Field(..., description="ID da severidade")
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

    # novo campo
    status: Optional[str] = Field(
        "pendente",
        description="Status da ocorrência: ativa, pendente, resolvida"
    )


class OccurrenceCreate(OccurrenceBase):
    pass


class OccurrenceResponse(OccurrenceBase):
    id: int
    user_id: int
    created_at: datetime
    severity: SeverityResponse

    model_config = ConfigDict(from_attributes=True)

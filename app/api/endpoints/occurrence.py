from typing import Annotated
from sqlalchemy.orm import Session

from fastapi import (
    APIRouter,
    Depends,
    status,
    File,
    UploadFile,
    Form,
    HTTPException,
)

# Core
from app.core.auth import get_current_user

# Database
from app.database.session import get_db

# Models
from app.models.user import User
from app.models.severity import Severity

# Schemas
from app.schemas.occurrence import OccurrenceResponse

# Services
from app.services.occurrence_service import OccurrenceService

# Repositories
from app.repositories.occurrence_repository import OccurrenceRepository


# Router configuration
router = APIRouter()


# Dependency annotations
CurrentSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]


def get_occurrence_repository(db: CurrentSession) -> OccurrenceRepository:
    return OccurrenceRepository(db)


OccurrenceRepo = Annotated[OccurrenceRepository, Depends(get_occurrence_repository)]


def get_occurrence_service(repo: OccurrenceRepo) -> OccurrenceService:
    return OccurrenceService(repo)


OccurrenceServiceDep = Annotated[OccurrenceService, Depends(get_occurrence_service)]


@router.post("", status_code=status.HTTP_201_CREATED, response_model=OccurrenceResponse)
async def create_occurrence(
    occurrence_service: OccurrenceServiceDep,
    current_user: CurrentUser,
    db: CurrentSession,
    name: Annotated[
        str,
        Form(
            description="Nome da ocorrência",
            min_length=1,
            max_length=100,
            examples=["Lixo acumulado na calçada"],
        ),
    ],
    category: Annotated[
        str,
        Form(
            description="Categoria da ocorrência",
            min_length=1,
            max_length=50,
            examples=["lixo", "enchente", "buraco"],
        ),
    ],
    severity_id: Annotated[
        int, Form(description="ID do nível de severidade", gt=0, examples=[1, 2, 3])
    ],
    latitude: Annotated[
        float,
        Form(description="Latitude da localização", ge=-90, le=90, examples=[-1.4558]),
    ],
    longitude: Annotated[
        float,
        Form(
            description="Longitude da localização", ge=-180, le=180, examples=[-48.4902]
        ),
    ],
    description: Annotated[
        str | None,
        Form(description="Descrição detalhada da ocorrência", max_length=1000),
    ] = None,
    image: Annotated[
        UploadFile | None,
        File(
            description="Imagem da ocorrência (opcional)",
        ),
    ] = None,
) -> OccurrenceResponse:
    severity = db.query(Severity).filter(Severity.id == severity_id).first()
    if not severity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Severity ID {severity_id} não encontrada. "
            f"Use o endpoint /severities para listar as opções válidas.",
        )

    # Validar tipo de arquivo se imagem foi fornecida
    if image:
        allowed_types = ["image/jpeg", "image/png", "image/webp", "image/jpg"]
        if image.content_type not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tipo de arquivo não suportado: {image.content_type}. "
                f"Use: {', '.join(allowed_types)}",
            )

        # Validar tamanho do arquivo (5MB max)
        max_size = 5 * 1024 * 1024  # 5MB
        image.file.seek(0, 2)  # Move para o final
        file_size = image.file.tell()
        image.file.seek(0)  # Volta para o início

        if file_size > max_size:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Arquivo muito grande. Tamanho máximo: 5MB",
            )

    # Preparar dados para criação
    occurrence_data = {
        "name": name.strip(),
        "category": category.strip().lower(),
        "description": description.strip() if description else None,
        "severity_id": severity_id,
        "latitude": latitude,
        "longitude": longitude,
        "status": "pendente"
    }

    # Criar ocorrência
    occurrence = occurrence_service.create_occurrence(
        user_id=current_user.id,
        data=occurrence_data,
        image=image,
    )

    return occurrence


@router.get(
    "/geojson",
    summary="Listar ocorrências em formato GeoJSON",
    description="Retorna todas as ocorrências cadastradas no formato GeoJSON, "
    "adequado para visualização em mapas. Inclui imagens em base64 para exibição direta.",
    responses={
        200: {
            "description": "Lista de ocorrências em formato GeoJSON",
            "content": {
                "application/json": {
                    "example": {
                        "type": "FeatureCollection",
                        "features": [
                            {
                                "type": "Feature",
                                "geometry": {
                                    "type": "Point",
                                    "coordinates": [-48.4902, -1.4558],
                                },
                                "properties": {
                                    "id": 1,
                                    "name": "Lixo acumulado",
                                    "category": "lixo",
                                    "severity": {
                                        "id": 2,
                                        "code": "MODERADA",
                                        "name": "Moderada",
                                        "color": "#FFA500",
                                    },
                                    "image_binary": "base64_string...",
                                    "image_mime_type": "image/jpeg"
                                },
                            }
                        ],
                    }
                }
            },
        }
    },
)
async def list_occurrences_geojson(
    occurrence_service: OccurrenceServiceDep,
) -> dict:
    """
    Lista todas as ocorrências em formato GeoJSON.

    O formato GeoJSON é adequado para integração com bibliotecas de mapas
    como Leaflet, Mapbox, Google Maps, etc. Cada ocorrência é retornada
    como uma Feature com geometria Point e propriedades detalhadas.

    Inclui as imagens em formato base64 para exibição direta no frontend.

    Args:
        occurrence_service: Serviço de ocorrências (injetado)

    Returns:
        dict: FeatureCollection GeoJSON com todas as ocorrências
    """
    return occurrence_service.list_occurrences_geojson()


@router.get(
    "/{occurrence_id}/image",
    summary="Obter imagem da ocorrência",
    description="Retorna a imagem binária de uma ocorrência específica.",
    responses={
        200: {
            "description": "Imagem binária da ocorrência",
            "content": {
                "image/jpeg": {},
                "image/png": {},
                "image/webp": {}
            }
        },
        404: {
            "description": "Ocorrência ou imagem não encontrada"
        }
    }
)
async def get_occurrence_image(
    occurrence_id: int,
    occurrence_service: OccurrenceServiceDep,
):
    """
    Retorna a imagem binária de uma ocorrência.

    Este endpoint é útil quando você quer carregar a imagem separadamente
    ou usar em tags <img> diretamente.

    Args:
        occurrence_id: ID da ocorrência
        occurrence_service: Serviço de ocorrências (injetado)

    Returns:
        Response: Imagem binária com o content-type apropriado
    """
    return occurrence_service.get_occurrence_image(occurrence_id)


@router.get(
    "/severities",
    summary="Listar níveis de severidade",
    description="Retorna todos os níveis de severidade disponíveis para "
    "classificação de ocorrências.",
    responses={
        200: {
            "description": "Lista de severidades disponíveis",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "code": "LEVE",
                            "name": "Leve",
                            "color": "#90EE90",
                            "order": 1,
                        },
                        {
                            "id": 2,
                            "code": "MODERADA",
                            "name": "Moderada",
                            "color": "#FFA500",
                            "order": 2,
                        },
                        {
                            "id": 3,
                            "code": "GRAVE",
                            "name": "Grave",
                            "color": "#FF0000",
                            "order": 3,
                        },
                    ]
                }
            },
        }
    },
)
async def list_severities(db: CurrentSession) -> list[dict]:
    """
    Lista todos os níveis de severidade disponíveis.

    Este endpoint retorna as opções de severidade que podem ser usadas
    ao criar uma nova ocorrência. As severidades são ordenadas por
    gravidade crescente.

    Args:
        db: Sessão do banco de dados (injetado)

    Returns:
        list[dict]: Lista de severidades com id, código, nome, cor e ordem
    """
    severities = db.query(Severity).order_by(Severity.order).all()

    return [
        {
            "id": severity.id,
            "code": severity.code,
            "name": severity.name,
            "color": severity.color,
            "order": severity.order,
        }
        for severity in severities
    ]
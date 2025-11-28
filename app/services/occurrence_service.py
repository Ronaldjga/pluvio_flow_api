from app.schemas.occurrence import OccurrenceCreate
from app.repositories.occurrence_repository import OccurrenceRepository
from fastapi import UploadFile, HTTPException
import os
from pathlib import Path
import base64
from fastapi.responses import Response

class OccurrenceService:
    def __init__(self, repository: OccurrenceRepository):
        self.repository = repository

    def create_occurrence(
        self,
        user_id: int,
        data: dict,
        image: UploadFile | None = None
    ):
        # Valida via Pydantic
        validated = OccurrenceCreate(**data)

        image_path = None

        if image:
            upload_dir = Path("uploads/occurrences")
            upload_dir.mkdir(parents=True, exist_ok=True)

            file_extension = os.path.splitext(image.filename)[1]
            filename = f"{user_id}_{validated.name}_{validated.latitude}_{validated.longitude}{file_extension}"
            file_path = upload_dir / filename

            with open(file_path, "wb") as f:
                f.write(image.file.read())

            image_path = str(file_path)

        # Cria a ocorrência no banco
        occurrence = self.repository.create(
            user_id=user_id,
            name=validated.name,
            category=validated.category,
            description=validated.description,
            severity_id=validated.severity_id,
            latitude=validated.latitude,
            longitude=validated.longitude,
            image_path=image_path,
            status=validated.status,
        )

        return occurrence

    def list_occurrences_geojson(self):
        occurrences = self.repository.get_all_with_user()
        
        features = []
        for occ in occurrences:
            # Lê a imagem do arquivo se existir e converte para base64
            image_binary = None
            image_mime_type = None
            
            if occ.image_path and os.path.exists(occ.image_path):
                try:
                    with open(occ.image_path, "rb") as f:
                        image_content = f.read()
                    image_binary = base64.b64encode(image_content).decode('utf-8')
                    
                    # Determina o MIME type baseado na extensão do arquivo
                    ext = os.path.splitext(occ.image_path)[1].lower()
                    mime_types = {
                        '.jpg': 'image/jpeg',
                        '.jpeg': 'image/jpeg',
                        '.png': 'image/png',
                        '.gif': 'image/gif',
                        '.bmp': 'image/bmp',
                        '.webp': 'image/webp'
                    }
                    image_mime_type = mime_types.get(ext, 'image/jpeg')
                    
                except Exception as e:
                    print(f"Erro ao ler imagem: {e}")

            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [occ.longitude, occ.latitude]
                },
                "properties": {
                    "id": occ.id,
                    "name": occ.name,
                    "category": occ.category,
                    "description": occ.description,
                    "severity": {
                        "id": occ.severity.id,
                        "code": occ.severity.code,
                        "name": occ.severity.name,
                        "color": occ.severity.color,
                    },
                    "status": occ.status,
                    "image_path": occ.image_path,
                    "image_binary": image_binary,  # Binário da imagem em base64
                    "image_mime_type": image_mime_type,  # Tipo MIME para exibição
                    "created_at": occ.created_at.isoformat(),
                    "user": {
                        "id": occ.user.id,
                        "username": occ.user.username,
                    }
                }
            })

        return {
            "type": "FeatureCollection",
            "features": features
        }

    def get_occurrence_image(self, occurrence_id: int):
        """Retorna a imagem binária de uma ocorrência específica"""
        occurrence = self.repository.get_by_id(occurrence_id)
        
        if not occurrence or not occurrence.image_path:
            raise HTTPException(status_code=404, detail="Imagem não encontrada")
        
        if not os.path.exists(occurrence.image_path):
            raise HTTPException(status_code=404, detail="Arquivo de imagem não encontrado")
        
        try:
            with open(occurrence.image_path, "rb") as f:
                image_content = f.read()
            
            # Determina o MIME type
            ext = os.path.splitext(occurrence.image_path)[1].lower()
            mime_types = {
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.png': 'image/png',
                '.gif': 'image/gif',
                '.bmp': 'image/bmp',
                '.webp': 'image/webp'
            }
            media_type = mime_types.get(ext, 'image/jpeg')
            
            return Response(content=image_content, media_type=media_type)
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao ler imagem: {str(e)}")
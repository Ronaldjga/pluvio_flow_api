from app.schemas.occurrence import OccurrenceCreate
from app.repositories.occurrence_repository import OccurrenceRepository
from fastapi import UploadFile
import os
from pathlib import Path

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

        # Agora envia o status também
        occurrence = self.repository.create(
            user_id=user_id,
            name=validated.name,
            category=validated.category,
            description=validated.description,
            severity_id=validated.severity_id,
            latitude=validated.latitude,
            longitude=validated.longitude,
            image_path=image_path,
            status=validated.status,  # 🔥 Importante
        )

        return occurrence

    def list_occurrences_geojson(self):
        occurrences = self.repository.get_all_with_user()
        
        features = []
        for occ in occurrences:
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
                    "status": occ.status,  # 🔥 retorna também
                    "image_path": occ.image_path,
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

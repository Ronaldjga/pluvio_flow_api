from fastapi import HTTPException, status
from app.repositories.occurrence_repository import OccurrenceRepository
from app.schemas.occurrence import OccurrenceCreate
from app.models.occurrence import Occurrence

class OccurrenceService:
    def __init__(self, occurrence_repo: OccurrenceRepository):
        self.occurrence_repo = occurrence_repo

    def create_occurrence(self, user_id: int, data: OccurrenceCreate) -> Occurrence:
        return self.occurrence_repo.create(user_id, data)

    def list_occurrences_geojson(self):
        occurrences = self.occurrence_repo.get_all()
        features = []
        for o in occurrences:
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [o.longitude, o.latitude]
                },
                "properties": {
                    "id": o.id,
                    "name": o.name,
                    "category": o.category,
                    "description": o.description,
                    "username": o.user.username,  # << alterado aqui
                    "created_at": o.created_at.isoformat(),
                }
            })
        return {"type": "FeatureCollection", "features": features}

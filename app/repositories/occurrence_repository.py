from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.occurrence import Occurrence
from app.schemas.occurrence import OccurrenceCreate

class OccurrenceRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: int, data: OccurrenceCreate) -> Occurrence:
        occurrence = Occurrence(
            user_id=user_id,
            name=data.name,
            category=data.category,
            description=data.description,
            latitude=data.latitude,
            longitude=data.longitude,
        )
        self.db.add(occurrence)
        self.db.commit()
        self.db.refresh(occurrence)
        return occurrence

    def get_all(self) -> List[Occurrence]:
        return self.db.query(Occurrence).all()

    def get_by_id(self, occurrence_id: int) -> Optional[Occurrence]:
        return self.db.query(Occurrence).filter(Occurrence.id == occurrence_id).first()

    def delete(self, occurrence_id: int):
        occurrence = self.get_by_id(occurrence_id)
        if occurrence:
            self.db.delete(occurrence)
            self.db.commit()
        return occurrence

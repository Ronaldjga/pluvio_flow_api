# app/repositories/occurrence_repository.py
from sqlalchemy.orm import Session, joinedload
from app.models.occurrence import Occurrence

class OccurrenceRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        user_id: int,
        name: str,
        category: str,
        description: str | None,
        severity_id: int,
        latitude: float,
        longitude: float,
        image_path: str | None = None,
        status: str = "pendente",  # 🔥 novo campo com default
    ) -> Occurrence:
        occurrence = Occurrence(
            user_id=user_id,
            name=name,
            category=category,
            description=description,
            severity_id=severity_id,
            latitude=latitude,
            longitude=longitude,
            image_path=image_path,
            status=status,  # 🔥 agora vai para o banco
        )
        
        self.db.add(occurrence)
        self.db.commit()
        self.db.refresh(occurrence)
        
        return occurrence

    def get_all_with_user(self):
        return (
            self.db.query(Occurrence)
            .options(
                joinedload(Occurrence.user),
                joinedload(Occurrence.severity)
            )
            .all()
        )
    
    def get_by_id(self, occurrence_id: int):
        return self.db.query(Occurrence).filter(Occurrence.id == occurrence_id).first()

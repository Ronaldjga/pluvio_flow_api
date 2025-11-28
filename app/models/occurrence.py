from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Occurrence(Base):
    __tablename__ = "occurrences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)

    image_path = Column(String(255), nullable=True)

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    severity_id = Column(Integer, ForeignKey("severities.id"), nullable=False)

    # novo campo
    status = Column(
        Enum("ativa", "pendente", "resolvida", name="occurrence_status"),
        default="pendente",
        nullable=False
    )

    severity = relationship("Severity", back_populates="occurrences")
    user = relationship("User", back_populates="occurrences")

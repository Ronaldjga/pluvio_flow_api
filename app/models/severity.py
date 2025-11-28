from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Severity(Base):
    __tablename__ = "severities"
    
    id = Column(Integer, primary_key=True)
    code = Column(String(20), unique=True, nullable=False)  # LEVE, MODERADA, GRAVE
    name = Column(String(50), nullable=False)  # Nome para exibição
    color = Column(String(7), nullable=True)  # Hex color: #FF0000
    order = Column(Integer, nullable=False)  # Para ordenação
    
    occurrences = relationship("Occurrence", back_populates="severity")
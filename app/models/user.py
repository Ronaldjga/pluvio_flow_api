from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    username = Column(String)
    cpf = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    
    occurrences = relationship("Occurrence", back_populates="user")


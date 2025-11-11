from typing import Optional
from app.models.user import User
from sqlalchemy.orm import Session
from app.database.session import get_db


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: str) -> Optional[User]:
        """Buscar usuario por id"""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, user_email: str) -> Optional[User]:
        """Buscar usuario por email"""
        return self.db.query(User).filter(User.email == user_email).first()

    def get_by_cpf(self, user_cpf: str) -> Optional[User]:
        """Buscar usuario por cpf"""
        return self.db.query(User).filter(User.cpf == user_cpf).first()

    def get_by_username(self, user_username: str) -> Optional[User]:
        """Buscar usuario por username"""
        return self.db.query(User).filter(User.username == user_username).first()

    # CREATE
    def create_user(self, name, username, email, cpf, password) -> User:
        user = User(
            name=name,
            username=username,
            email=email,
            cpf=cpf,
            password=password,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

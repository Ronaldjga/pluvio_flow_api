from fastapi import HTTPException, status
from app.core.security import verify_password, create_access_token
from app.repositories.user_repository import UserRepository
from app.core.security import get_password_hash


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def authenticate_user(self, username: str, password: str):
        user = self.user_repo.get_by_username(username)
        if not user or not verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )

        token = create_access_token({"sub": user.username})
        return {"access_token": token, "token_type": "bearer"}

    def register_user(self, name, username, email, cpf, password):
        # verifica se o usuário já existe
        if self.user_repo.get_by_cpf(cpf):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cpf already registered",
            )

        if self.user_repo.get_by_username(username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exist",
            )
            
        if self.user_repo.get_by_email(email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        hashed_password = get_password_hash(password)

        user = self.user_repo.create_user(
            name=name,
            username=username,
            email=email,
            cpf=cpf,
            password=hashed_password,
        )

        token = create_access_token({"sub": user.username})
        return {"access_token": token, "token_type": "bearer"}

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    name: str
    username: str = Field(min_length=3, max_length=15)
    email: EmailStr
    cpf: str = Field(min_length=11, max_length=11,)
    password: str = Field(min_length=6, max_length=128)


class LoginRequest(BaseModel):
    username: str = Field(min_length=3, max_length=15)
    password: str = Field(min_length=6, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

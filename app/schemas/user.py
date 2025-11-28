from pydantic import BaseModel, EmailStr, ConfigDict, Field


class UserBase(BaseModel):
    name: str
    username: str = Field(min_length=3, max_length=15)
    email: EmailStr
    cpf: str = Field(
        min_length=11,
        max_length=11,
    )


class UserResponse(UserBase):
    id: int
    name: str
    username: str = Field(min_length=3, max_length=15)
    email: EmailStr
    cpf: str = Field(
        min_length=11,
        max_length=11,
    )

from pydantic import BaseModel, EmailStr, ConfigDict

from app.models.user import UserRole
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    role: UserRole


class UserLogin(BaseModel):
    email: EmailStr
    password: str
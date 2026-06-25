from pydantic import BaseModel, EmailStr, ConfigDict
from app.models.user import UserRole


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str
    role: UserRole = UserRole.EXECUTOR


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    role: UserRole


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = None


# PUT /users/{id}/role (only admin)
class UserRoleUpdate(BaseModel):  
    role: UserRole
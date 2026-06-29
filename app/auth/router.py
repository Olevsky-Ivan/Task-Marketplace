from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schemas import Token, UserLogin
from app.auth.service import authenticate_user
from app.auth.security import create_access_token
from app.core.config import settings
from app.database.session import get_db
from app.users.service import UserService
from app.users.repository import UserRepository
from app.users.schemas import UserCreate, UserRead
from app.wallet.service import WalletService
from app.wallet.repository import WalletRepository

router = APIRouter()

user_service = UserService(
    repository=UserRepository(),
    wallet_service=WalletService(repository=WalletRepository()),
)


@router.post("/register", response_model=UserRead)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    return await user_service.create_user(db, user_data)


@router.post("/login", response_model=Token)
async def login(
    user_data: UserLogin,
    db: AsyncSession = Depends(get_db),
):
    user = await authenticate_user(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}

from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.wallet.service import WalletService
from app.wallet.repository import WalletRepository
from app.wallet.schemas import WalletRead, DepositRequest, TransactionRead

router = APIRouter()

wallet_service = WalletService(repository=WalletRepository())


@router.get("/me", response_model=WalletRead)
async def get_my_wallet(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await wallet_service.get_my_wallet(db, current_user.id)


@router.post("/deposit", response_model=WalletRead)
async def deposit(
    body: DepositRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await wallet_service.deposit(db, current_user.id, body.amount)


@router.get("/transactions", response_model=list[TransactionRead])
async def get_transactions(
    limit: int = 10,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await wallet_service.get_transactions(db, current_user.id, limit, offset)

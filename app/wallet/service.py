from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.wallet import Wallet
from app.wallet.repository import WalletRepository


class WalletService:

    def __init__(self, repository: WalletRepository):
        self.repository = repository

    async def _get_wallet_or_404(
        self,
        db: AsyncSession,
        user_id: int,
        *,
        for_update: bool = False,
    ) -> Wallet:
        if for_update:
            wallet = await self.repository.get_by_user_id_for_update(
                db,
                user_id,
            )
        else:
            wallet = await self.repository.get_by_user_id(
                db,
                user_id,
            )

        if not wallet:
            raise HTTPException(
                status_code=404,
                detail="Wallet not found",
            )

        return wallet

    async def create_wallet(
        self,
        db: AsyncSession,
        user_id: int,
    ) -> Wallet:
        existing = await self.repository.get_by_user_id(db, user_id)

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Wallet already exists",
            )

        return await self.repository.create_wallet(db, user_id)

    async def get_my_wallet(
        self,
        db: AsyncSession,
        user_id: int,
    ) -> Wallet:
        return await self._get_wallet_or_404(db, user_id)

    async def deposit(
        self,
        db: AsyncSession,
        user_id: int,
        amount: Decimal,
    ) -> Wallet:
        if amount <= 0:
            raise HTTPException(
                status_code=400,
                detail="Amount must be positive",
            )

        wallet = await self._get_wallet_or_404(
            db,
            user_id,
            for_update=True,
        )

        wallet.balance += amount

        await self.repository.create_transaction(
            db,
            wallet.id,
            amount,
            "deposit",
            description="Manual deposit",
        )

        await db.commit()
        await db.refresh(wallet)

        return wallet

    async def freeze(
        self,
        db: AsyncSession,
        user_id: int,
        amount: Decimal,
    ) -> None:
        if amount <= 0:
            raise HTTPException(
                status_code=400,
                detail="Amount must be positive",
            )

        wallet = await self._get_wallet_or_404(
            db,
            user_id,
            for_update=True,
        )

        if wallet.balance < amount:
            raise HTTPException(
                status_code=400,
                detail="Insufficient funds",
            )

        wallet.balance -= amount
        wallet.frozen_balance += amount

        await self.repository.create_transaction(
            db,
            wallet.id,
            amount,
            "freeze",
            description="Funds frozen for task",
        )

    async def transfer_on_approve(
        self,
        db: AsyncSession,
        task_id: int,
        customer_id: int,
        executor_id: int,
        amount: Decimal,
    ) -> None:
        customer_wallet = await self._get_wallet_or_404(
            db,
            customer_id,
            for_update=True,
        )

        executor_wallet = await self._get_wallet_or_404(
            db,
            executor_id,
            for_update=True,
        )

        if customer_wallet.frozen_balance < amount:
            raise HTTPException(
                status_code=400,
                detail="Insufficient frozen funds",
            )

        customer_wallet.frozen_balance -= amount

        await self.repository.create_transaction(
            db,
            customer_wallet.id,
            -amount,
            "transfer_out",
            description=f"Payment for task #{task_id}",
        )

        executor_wallet.balance += amount

        await self.repository.create_transaction(
            db,
            executor_wallet.id,
            amount,
            "transfer_in",
            description=f"Payment for task #{task_id}",
        )

    async def unfreeze_on_cancel(
        self,
        db: AsyncSession,
        user_id: int,
        amount: Decimal,
    ) -> None:
        wallet = await self._get_wallet_or_404(
            db,
            user_id,
            for_update=True,
        )

        if wallet.frozen_balance < amount:
            raise HTTPException(
                status_code=400,
                detail="Insufficient frozen funds",
            )

        wallet.frozen_balance -= amount
        wallet.balance += amount

        await self.repository.create_transaction(
            db,
            wallet.id,
            amount,
            "unfreeze",
            description="Funds returned after task cancellation",
        )

    async def get_transactions(
        self,
        db: AsyncSession,
        user_id: int,
        limit: int,
        offset: int,
    ) -> list:
        wallet = await self._get_wallet_or_404(
            db,
            user_id,
        )

        return await self.repository.get_transactions(
            db,
            wallet.id,
            limit,
            offset,
        )
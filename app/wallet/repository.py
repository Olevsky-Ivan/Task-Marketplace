from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.wallet import Wallet
from app.models.transaction import Transaction


class WalletRepository:

    async def get_by_user_id(self, db: AsyncSession, user_id: int) -> Wallet | None:
        result = await db.execute(select(Wallet).where(Wallet.user_id == user_id))
        return result.scalar_one_or_none()

    async def create_wallet(self, db: AsyncSession, user_id: int) -> Wallet:
        wallet = Wallet(
            user_id=user_id,
            balance=Decimal("0.00"),
            frozen_balance=Decimal("0.00"),
        )
        db.add(wallet)
        await db.flush()
        await db.refresh(wallet)
        return wallet

    async def create_transaction(
        self,
        db: AsyncSession,
        wallet_id: int,
        amount: Decimal,
        type: str,
        description: str | None = None,
    ) -> Transaction:
        tx = Transaction(
            wallet_id=wallet_id,
            amount=amount,
            type=type,
            description=description,
        )
        db.add(tx)
        await db.flush()
        return tx

    async def get_transactions(
        self,
        db: AsyncSession,
        wallet_id: int,
        limit: int,
        offset: int,
    ) -> list[Transaction]:
        result = await db.execute(
            select(Transaction)
            .where(Transaction.wallet_id == wallet_id)
            .order_by(Transaction.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()

    async def get_by_user_id_for_update(
        self,
        db: AsyncSession,
        user_id: int,
    ) -> Wallet | None:
        result = await db.execute(
            select(Wallet)
            .where(Wallet.user_id == user_id)
            .with_for_update()
        )
        return result.scalar_one_or_none()
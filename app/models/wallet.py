from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

class Wallet(Base):
    __tablename__ = "wallets"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True
    )

    balance: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=0
    )

    frozen_balance: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=0
    )

    user = relationship("User", back_populates="wallet")
from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, String, DateTime, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)

    wallet_id: Mapped[int] = mapped_column(
        ForeignKey("wallets.id"),
        nullable=False
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    type: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )
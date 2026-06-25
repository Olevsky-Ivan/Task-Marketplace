from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from datetime import datetime


class WalletRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    balance: Decimal
    frozen_balance: Decimal


class DepositRequest(BaseModel):
    amount: Decimal

    model_config = ConfigDict(
        json_schema_extra={"example": {"amount": "100.00"}}
    )


class TransactionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    wallet_id: int
    amount: Decimal
    type: str
    description: str | None
    created_at: datetime
from datetime import datetime

from sqlalchemy import String, DateTime, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from enum import Enum



class UserRole(str, Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"
    EXECUTOR = "executor"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole),
        nullable=False,
        default=UserRole.EXECUTOR,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    wallet = relationship(
        "Wallet",
        back_populates="user",
        uselist=False,
    )

    tasks_created = relationship(
        "Task",
        back_populates="creator",
        foreign_keys="Task.creator_id",
    )

    tasks_assigned = relationship(
        "Task",
        back_populates="executor",
        foreign_keys="Task.executor_id",
    )

    attachments = relationship(
        "Attachment",
        back_populates="user",
    )

    comments = relationship(
        "Comment",
        back_populates="user",
    )
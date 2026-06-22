from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    role: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="executor"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    wallet = relationship(
        "Wallet",
        back_populates="user",
        uselist=False
    )

    tasks_created = relationship(
        "Task",
        back_populates="creator",
        foreign_keys="Task.creator_id"
    )

    tasks_assigned = relationship(
        "Task",
        back_populates="executor",
        foreign_keys="Task.executor_id"
    )

    attachments = relationship(
        "Attachment",
        back_populates="user"
    )

    comments = relationship(
        "Comment",
        back_populates="user"
    )
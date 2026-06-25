from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base
from app.models.tag import task_tags

from decimal import Decimal
from sqlalchemy import Numeric, DateTime

from datetime import datetime, timezone


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="open")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    executor_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    reward: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=True)

    creator = relationship("User", back_populates="tasks_created", foreign_keys=[creator_id])
    executor = relationship("User", back_populates="tasks_assigned", foreign_keys=[executor_id])
    comments = relationship("Comment", back_populates="task")
    category = relationship("Category")
    tags = relationship("Tag", secondary=task_tags, lazy="selectin")
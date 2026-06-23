from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(255), nullable=False)

    description: Mapped[str] = mapped_column(String, nullable=True)

    status: Mapped[str] = mapped_column(
        String(50),
        default="open"
    )

    creator_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    executor_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    creator = relationship(
        "User",
        back_populates="tasks_created",
        foreign_keys=[creator_id]
    )

    executor = relationship(
        "User",
        back_populates="tasks_assigned",
        foreign_keys=[executor_id]
    )

    attachments = relationship(
        "Attachment",
        back_populates="task"
    )

    comments = relationship(
        "Comment",
        back_populates="task"
    )
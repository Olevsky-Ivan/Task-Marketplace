from datetime import datetime

from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base


class Category(Base):

    __tablename__="categories"


    id: Mapped[int] = mapped_column(
        primary_key=True
    )


    name: Mapped[str]
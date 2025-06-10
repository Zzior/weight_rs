from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Abstract model with declarative base functionality."""
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)


class Temp(Base):
    __tablename__ = "temp"
    date: Mapped[datetime] = mapped_column(sa.DateTime, unique=False, nullable=False)
    weight: Mapped[int] = mapped_column(sa.Integer, unique=False, nullable=False)

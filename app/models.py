from decimal import Decimal
from datetime import date as date_type

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Numeric, String


class Base(DeclarativeBase):
    pass


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    type: Mapped[str] = mapped_column(String(10))
    date: Mapped[date_type]
    merchant: Mapped[str]
    category: Mapped[str]
    description: Mapped[str | None]

from decimal import Decimal
from datetime import date as date_type

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Numeric, String, ForeignKey


class Base(DeclarativeBase):
    pass


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    type: Mapped[str] = mapped_column(String(10))
    date: Mapped[date_type]
    merchant: Mapped[str]
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    description: Mapped[str | None]
    category: Mapped["Category"] = relationship(back_populates="transactions")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="category")

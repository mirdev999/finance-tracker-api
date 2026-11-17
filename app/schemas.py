from enum import Enum
from datetime import date as date_type
from typing import Annotated
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict


class TransactionType(str, Enum):

    INCOME = "income"
    EXPENSE = "expense"


class TransactionCreate(BaseModel):

    amount: Annotated[
        Decimal,
        Field(
            gt=0,
            decimal_places=2,
            max_digits=12,
            description="Input/output flow of money is a decimal and greater than 0",
        ),
    ]
    type: Annotated[TransactionType, Field(description="Is an expense or an income?")]
    date: Annotated[
        date_type, Field(description="When the spend(t)/earn(ed) an expense/income")
    ]
    merchant: Annotated[
        str,
        Field(
            min_length=1,
            description="From/to who (company/person) comes/goes the money",
        ),
    ]
    category_id: Annotated[
        int,
        Field(
            gt=0,
            description="ID of the category this transaction belongs to",
        ),
    ]
    description: Annotated[
        str | None, Field(description="Information about the whole transaction")
    ] = None


class TransactionOut(TransactionCreate):

    model_config = ConfigDict(from_attributes=True)
    id: Annotated[int, Field(description="This is id for each transaction")]


class CategoryCreate(BaseModel):

    name: Annotated[str, Field(min_length=1, max_length=50)]


class CategoryOut(CategoryCreate):

    model_config = ConfigDict(from_attributes=True)
    id: Annotated[int, Field(description="This is the id for each category")]


class AccountCreate(BaseModel):

    name: Annotated[str, Field(min_length=1, max_length=50)]


class AccountOut(AccountCreate):

    model_config = ConfigDict(from_attributes=True)
    id: Annotated[int, Field(description="this is the id for each account")]

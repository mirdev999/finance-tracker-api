from enum import Enum
from pydantic import BaseModel, Field
from datetime import date as date_type
from typing import Annotated
from decimal import Decimal


class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"

class TransactionCreate(BaseModel):

    amount: Annotated[Decimal,Field(gt=0,decimal_places=2,max_digits=12,description="input/output flow of money is a decimal and greater than 0")]
    type: Annotated[TransactionType,Field(description="is an expense or an income?")]
    date: Annotated[date_type,Field(description="when the spend(t)/earn(ed) an expense/income")]
    merchant: Annotated[str,Field(min_length=1,description="from/to who (company/person) comes/goes the money")]
    category: Annotated[str,Field(min_length=1,description="Which category of expense/income does this apply to?")]
    description: Annotated[str|None,Field(description="information about the whole transaction")]= None

class TransactionOut(TransactionCreate):

    id: Annotated[int,Field(description="This is id for each transaction")]


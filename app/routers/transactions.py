from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from app.schemas import TransactionOut, TransactionCreate

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Transaction

router = APIRouter(prefix="/transactions", tags=["transactions"])

transactions_db = []


async def get_transaction_or_404(transaction_id: int):
    for transaction in transactions_db:
        if transaction["id"] == transaction_id:
            return transaction
    raise HTTPException(status_code=404, detail="Transaction not found")


@router.post("", status_code=201, response_model=TransactionOut)
def create_transaction(
    transaction_in: TransactionCreate, session: Annotated[Session, Depends(get_db)]
):
    data = transaction_in.model_dump()
    new_transaction = Transaction(**data)
    session.add(new_transaction)
    session.commit()
    session.refresh(new_transaction)
    return new_transaction


@router.get("", response_model=list[TransactionOut])
def list_transactions(session: Annotated[Session, Depends(get_db)]):
    return session.scalars(select(Transaction)).all()


@router.get("/{transaction_id}", response_model=TransactionOut)
async def get_transaction(
    transaction: Annotated[dict, Depends(get_transaction_or_404)],
):
    return transaction


@router.delete("/{transaction_id}", status_code=204)
async def delete_transaction(
    transaction_to_delete: Annotated[dict, Depends(get_transaction_or_404)],
):
    transactions_db.remove(transaction_to_delete)
    return


@router.put("/{transaction_id}", response_model=TransactionOut)
async def update_transaction(
    transaction_in: TransactionCreate,
    transaction_to_update: Annotated[dict, Depends(get_transaction_or_404)],
):
    request_dict = transaction_in.model_dump()
    transaction_to_update.update(request_dict)
    return transaction_to_update

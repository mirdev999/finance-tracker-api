from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Transaction
from app.schemas import TransactionOut, TransactionCreate

router = APIRouter(prefix="/transactions", tags=["transactions"])


def get_transaction_or_404(
    transaction_id: int, session: Annotated[Session, Depends(get_db)]
):
    targeted_transaction = session.get(Transaction, transaction_id)
    if targeted_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return targeted_transaction


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
    return session.scalars(
        select(Transaction).order_by(Transaction.date.desc(), Transaction.id.desc())
    ).all()


@router.get("/{transaction_id}", response_model=TransactionOut)
def get_transaction(
    transaction: Annotated[Transaction, Depends(get_transaction_or_404)],
):
    return transaction


@router.delete("/{transaction_id}", status_code=204)
def delete_transaction(
    transaction_to_delete: Annotated[Transaction, Depends(get_transaction_or_404)],
    session: Annotated[Session, Depends(get_db)],
):
    session.delete(transaction_to_delete)
    session.commit()


@router.put("/{transaction_id}", response_model=TransactionOut)
def update_transaction(
    transaction_in: TransactionCreate,
    transaction_to_update: Annotated[Transaction, Depends(get_transaction_or_404)],
    session: Annotated[Session, Depends(get_db)],
):
    transac_dict = transaction_in.model_dump()
    for field, value in transac_dict.items():
        setattr(transaction_to_update, field, value)
    session.commit()
    session.refresh(transaction_to_update)
    return transaction_to_update

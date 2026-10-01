from fastapi import APIRouter, HTTPException, Depends
from app.schemas import TransactionOut, TransactionCreate
from typing import Annotated

router = APIRouter(prefix="/transactions", tags=["transactions"])

transactions_db = []


async def get_transaction_or_404(transaction_id: int):
    for transaction in transactions_db:
        if transaction["id"] == transaction_id:
            return transaction
    raise HTTPException(status_code=404, detail="Transaction not found")


@router.post("", status_code=201, response_model=TransactionOut)
async def create_transaction(transaction: TransactionCreate):

    request_dict = transaction.model_dump()
    existing_ids = [t["id"] for t in transactions_db]
    request_dict["id"] = max(existing_ids, default=0) + 1
    transactions_db.append(request_dict)
    return request_dict


@router.get("", response_model=list[TransactionOut])
async def list_transactions():
    return transactions_db


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

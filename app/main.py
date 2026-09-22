from fastapi import FastAPI, HTTPException, status, Response
from app.schemas import TransactionCreate, TransactionOut

app = FastAPI()

transactions_db = []

@app.post("/transactions",status_code=201, response_model=TransactionOut)
async def create_transaction(transaction : TransactionCreate):

    request_dict = transaction.model_dump()
    existing_ids = [t["id"] for t in transactions_db]
    request_dict["id"] = max(existing_ids,default=0)+1

    transactions_db.append(request_dict)
    return request_dict

@app.get("/transactions",response_model=list[TransactionOut])
async def list_transaction():
    return transactions_db

@app.get("/transactions/{transaction_id}",response_model=TransactionOut)
async def get_by_id(transaction_id:int):
    for transaction in transactions_db:
        if transaction["id"] == transaction_id:
            return transaction
    raise HTTPException(status_code=404,detail="Transaction not found")

@app.delete("/transactions/{transaction_id}", status_code=204)
async def delete_transaction(transaction_id : int):
    for transaction_to_delete in transactions_db:
        if transaction_to_delete["id"] == transaction_id:
            transactions_db.remove(transaction_to_delete)
            return
    raise HTTPException(status_code=404,detail="Transaction not found")

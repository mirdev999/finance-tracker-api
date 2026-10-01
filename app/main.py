from fastapi import FastAPI
from app.routers import transactions

app = FastAPI()

app.include_router(transactions.router)

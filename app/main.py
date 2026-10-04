from fastapi import FastAPI
from app.routers import transactions
from app.config import settings

app = FastAPI(title=settings.app_name)

app.include_router(transactions.router)
